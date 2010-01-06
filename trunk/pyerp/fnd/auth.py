# -*- coding: utf-8 -*- 


from datetime import datetime, date
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q as Q

from django.contrib.auth import models as dj_auth_models
from django.contrib import auth as dj_auth

from pyerp.fnd import models as fnd_models
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


BACKEND_SESSION_KEY = '_auth_user_backend'

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

class FndUserBackend(object):
    
    def authenticate(self, username=None, password=None):
        try:
            user = fnd_models.User.objects.get(Q(username=username), Q(is_active=True), 
                                    Q(start_date_active__lte=date.today()),           # 有效日期
                                    Q(Q(end_date_active__isnull=True) | 
                                      Q(end_date_active__gte=date.today())), 
                                    )
            if user.check_password(password):
                return user
        except fnd_models.User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return fnd_models.User.objects.get(pk=user_id)
        except fnd_models.User.DoesNotExist:
            return None

def login(request, user):
    if user is not None and user.pwd_expiration_type==2:
        user.pwd_accesses = user.pwd_accesses + 1  # 访问次数
    # save user's last login time, and bind to session 
    dj_auth.login(request, user);

def logout(request):
    dj_auth.logout(request)

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
