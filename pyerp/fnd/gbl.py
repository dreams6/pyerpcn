# -*- coding: utf-8 -*- 

"""
maybe a better solution
http://code.djangoproject.com/wiki/CookBookThreadlocalsAndUser

"""



try:
    import thread
except ImportError:
    import dummy_thread as thread
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.

from django.conf import settings

class GlobalManagementError(Exception):
    """
    This exception is thrown when something bad happens with global
    management.
    """
    pass

class ThreadFndGlobal(object):

    def __init__(self):
        self.thread_context = {}

    def get_user_id(self):
        """
        取得当前线程用户ID.
        """
        return self.get_attr('user_id', -1)
    user_id = property(get_user_id) 

    def get_user(self):
        """
        取得当前线程用户.
        """
        usr = self.get_attr('user', None)
        if usr is None:
            from pyerp.fnd.models import AnonymousUser, User
            if self.user_id==-1:
                usr = AnonymousUser()
            else:
                try:
                    usr = User.objects.get(pk=self.user_id)
                except User.DoesNotExist:
                    usr = AnonymousUser()
            self.set_attr('user', usr)
        return usr
    user = property(get_user) 

    def get_session(self):
        """
        取得当前线程Http回话.
        """
        return self.get_attr('session', None)
    session = property(get_session) 

    def get_resp_id(self):
        return self.get_attr('resp_id', -1)
    resp_id = property(get_resp_id) 

    def get_menu_id(self):
        return self.get_attr('menu_id', -1)
    menu_id = property(get_menu_id) 

    def get_function_id(self):
        return self.get_attr('function_id', -1)
    function_id = property(get_function_id) 

    def get_function(self):
        """
        取得当前线程访问的function.
        """
        return self.get_attr('function', None)
    function = property(get_function) 

    def set_resp_id(self, value):
        self.set_attr('resp_id', value)

    def set_menu_id(self, value):
        self.set_attr('menu_id', value)

    def set_function(self, value):
        self.set_attr('function_id', value and value.id or -1)
        self.set_attr('function', value)

    def get_org_id(self):
        if 'org_id' in self.thread_context[thread_ident]:
            return self.thread_context[thread_ident]['org_id']
        # TODO 从profile中取得组织ID
        orgid = 120
        self.thread_context[thread_ident]['org_id'] = orgid
        return orgid
    org_id = property(get_org_id) 

    def get_language(self):
        """
        返回用户使用的语言.
        """
        return self.session['language']
    language = property(get_language) 

    def get_appl_id(self):
        return -1
    appl_id = property(get_appl_id) 

    def get_site_id(self):
        """
        这里的site指的是,使用多站点时,各个站点的ID.而非site控制器.
        """
        return settings.SITE_ID
    site_id = property(get_site_id) 

    def get_server_id(self):
        return -1
    server_id = property(get_server_id) 

    def get_context_prefix(self):
        """
        取得当前context_prefix前缀, 使用mod_python时设定,context前缀
        """
        return self.get_attr('context_prefix', '/')
    context_prefix = property(get_context_prefix) 

    def get_site_prefix(self):
        """
        取得当前site控制器前缀
        """
        return self.get_attr('site_prefix', '')
    site_prefix = property(get_site_prefix) 

    def get_thread_id(self):
        """
        取得当前的线程ID
        """
        return thread.get_ident()
    thread_id = property(get_thread_id) 

    def get_attrs(self):
        """
        取得当前线程级变量字典
        """
        return self.thread_context[thread.get_ident()]
    attrs = property(get_attrs) 

    def get_attr(self, key, default=None):
        """
        根据指定key从当前线程变量中取得数据
        """
        thread_ident = thread.get_ident()
        if thread_ident in self.thread_context:
            if key in self.thread_context[thread_ident]: # and self.thread_context[thread_ident][key]:
                return self.thread_context[thread_ident][key]
            else:
                return default
        else:
            raise GlobalManagementError("This code isn't under global management. Please execute <gbl.enter_global_management> first.")

    def set_attr(self, key, value):
        """
        设定一个变量到线程级变量字典中
        """
        thread_ident = thread.get_ident()
        if thread_ident in self.thread_context:
            self.thread_context[thread_ident][key] = value
        else:
            raise GlobalManagementError("This code isn't under global management")

    def enter_global_management(self, user_id=-1, user=None, session=None):
        """
        Enters global management for a running thread. It must be balanced with
        the appropriate leave_global_management call, since the actual state is
        managed as a stack.
    
        The state and dirty flag are carried over from the surrounding block or
        from the settings, if there is no surrounding block (dirty is always false
        when no current block is running).
        """
        thread_ident = thread.get_ident()
        if thread_ident not in self.thread_context:
            self.thread_context[thread_ident] = {}

        if user is not None:
            self.set_attr('user_id', user.id)
            self.set_attr('user', user)
        else:
            # self.thread_context[thread_ident]["user_id"] = user_id
            self.set_attr('user_id', user_id)

        if session is not None:
            self.set_attr('session', session)

    def leave_global_management(self):
        """
        Leaves transaction management for a running thread. A dirty flag is carried
        over to the surrounding block, as a commit will commit all changes, even
        those from outside. (Commits are on connection level.)
        """
        thread_ident = thread.get_ident()
        if thread_ident in self.thread_context:
            del self.thread_context[thread_ident]
        else:
            raise GlobalManagementError("This code isn't under global management")

fnd_global = ThreadFndGlobal()
