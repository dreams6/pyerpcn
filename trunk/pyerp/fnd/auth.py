# -*- coding: utf-8 -*- 


from datetime import datetime, date
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q as Q

from pyerp.fnd.models import AnonymousUser, User


SESSION_KEY = '_fnd_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
REDIRECT_FIELD_NAME = 'next'

def load_backend(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = __import__(module, {}, {}, [attr])
    except ImportError, e:
        raise ImproperlyConfigured, 'Error importing authentication backend %s: "%s"' % (module, e)
    except ValueError, e:
        raise ImproperlyConfigured, 'Error importing authentication backends. Is AUTHENTICATION_BACKENDS a correctly defined list or tuple?'
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured, 'Module "%s" does not define a "%s" authentication backend' % (module, attr)
    return cls()

def get_backends():
    from django.conf import settings
    backends = []
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        backends.append(load_backend(backend_path))
    return backends


def authenticate(login_id=None, password=None):
    try:
        user = User.objects.get(Q(login_id=login_id), 
                                Q(start_date_active__lte=date.today()),           # 有效日期
                                Q(Q(end_date_active__isnull=True) | 
                                  Q(end_date_active__gte=date.today())), 
                                )
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None

def login(request, user):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request.
    """
    if user is None:
        user = request.user
    # TODO: It would be nice to support different login methods, like signed cookies.
    
    if user.pwd_expiration_type==2:   # 访问次数
        user.pwd_accesses = user.pwd_accesses + 1
    user.last_login = datetime.now()
    user.save()

    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != user.id:
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = user.id
    if hasattr(request, 'user'):
        request.user = user

def logout(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    request.session.flush()
    if hasattr(request, 'user'):
        request.user = AnonymousUser()

def get_user(request):
    try:
        user_id = request.session[SESSION_KEY]
        #backend_path = request.session[BACKEND_SESSION_KEY]
        #backend = load_backend(backend_path)
        #user = backend.get_user(user_id) or AnonymousUser()
        user = User.objects.get(pk=user_id)
    except (KeyError, User.DoesNotExist):
        user = AnonymousUser()
    return user


def has_resp(request, resp):
    """
    判断用户是否有指定的职责。
    
    """
    from pyerp.fnd.models import UserResp
    try:
        UserResp.objects.get(user=request.user, resp=resp)
        return resp 
    except UserResp.DoesNotExist:
        return None

def fun_in_resp(func, resp, p_menu=None):
    """
    递归检查指定的职责是否包含制定的function
    """
    from pyerp.fnd.models import MenuItem
    if p_menu is None:
        p_menu = resp.menu
    try:
        MenuItem.objects.get(Q(p_menu=p_menu), Q(function=func))
        return True
    except MenuItem.DoesNotExist:
        menu_item_list = MenuItem.objects.filter(Q(p_menu=p_menu), Q(submenu__isnull=False), Q(function__isnull=True))
        for mi in menu_item_list:
            if fun_in_resp(func, None, mi.submenu):
                return True
        return False
    except MenuItem.MultipleObjectsReturned:  # TODO
        return True
