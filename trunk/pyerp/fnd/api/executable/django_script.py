# -*- coding: utf-8 -*- 
import os, sys, time, StringIO

from pyerp.fnd import models as fnd_models
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


def main():
    # 取得请求id
    request_id = sys.argv[1]
    # 取得请求对象
    cr = fnd_models.ConcurrentRequest.objects.get(pk=request_id)

    # 重定向标准IO /.pyerp/ConcurrentRequest/%s  % request_id
    io_path = os.path.join(os.path.expanduser("~"), ".pyerp", 
                           "ConcurrentRequest", request_id)
    os.makedirs(io_path)
    sys.stdin = StringIO.StringIO()
    sys.stdout = open(os.path.join(io_path, "out"), "w+")
    sys.stderr = open(os.path.join(io_path, "err"), "w+")

    # 初始化fnd上下文
    request_user_id = cr.created_by
    fnd_global.enter_global_management(user_id=request_user_id)
    fnd_global.set_resp_id(cr.responsibility_id)

    # 更新进程id
    cr.os_process_id = os.getpid()
    cr.phase_code = "b"   # 开始执行
    cr.save()

    _file = cr.executable_file.split(".")
    executable_mod = __import__(".".join(_file[:-1]), {}, {}, [''])
    executable_func = getattr(executable_mod, _file[-1]) 
    kwargs = {}
    executable_func(**kwargs) # args
    cr.phase_code = "e"   # 结束
    cr.save()
    
    fnd_global.leave_global_management()

if __name__ == '__main__':
    # 启动ConcurrentRequest
    main()
