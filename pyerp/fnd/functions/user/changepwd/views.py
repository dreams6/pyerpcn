# -*- coding: utf-8 -*- 
from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


def display_main(request):
    message = ''
    
    if request.POST.has_key('confirm'):
        old_password = request.POST.get('old_password', None)
        new_password = request.POST.get('new_password', None)
        new_password1 = request.POST.get('new_password1', None)
        if not fnd_global.user.check_password(old_password):
            message = '密码错误.'
        else:
            if new_password:
                if new_password != new_password1:
                    message = '新密码和新密码确认不同,请重新输入.'
                else:
                    
                    message = '修改成功,您的新密码已经生效.'
                    fnd_global.user.reset_password(new_password)
            else:
                message = '请输入新密码.'

    context = {
        'app_path': request.get_full_path(),
        'message': message,
    }
    return fnd_render_to_response('user/changepwd/index.html', context)


