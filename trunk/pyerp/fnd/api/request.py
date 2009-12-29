# -*- coding: utf-8 -*- 

from pyerp.fnd.models import ConcurrentRequest, ConcurrentProgram


def submit_request(program_id):
    
    cp = ConcurrentProgram.objects.get(pk=program_id)
    ce = cp.executable
    
    # create a new concurrent request to model ConcurrentRequest
    cr = ConcurrentRequest()
    # cr.os_process_id = 
    cr.phase_code = 'p'   # 准备中
    cr.status_code = 'n'   # 正常
    cr.program_id = cp.program_id
    cr.output_file_mime = cp.output_file_mime
    cr.executable_id      = ce.executable_id
    cr.executable_method  = ce.method
    cr.executable_file    = ce.file
    cr.save()

    if ce.method=="django_script":
        # run the job in anthoer subprocess
        import os, sys, subprocess
        from pyerp.fnd.api.executable import django_script
        if not os.environ.has_key("DJANGO_SETTINGS_MODULE"):
            from django.conf import settings
            os.environ["DJANGO_SETTINGS_MODULE"] = settings.SETTINGS_MODULE
        if not os.environ.has_key("PYTHONPATH"):
            os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)

        if sys.platform == 'win32':
            # 利用子进程执行,django_script  env=None
            process = subprocess.Popen([sys.executable, django_script.__file__, str(cr.request_id)],
                                       env=os.environ)
            # cmd.exe /c start "" "{0}"
#            process = subprocess.Popen(["cmd", "/c", "start", sys.executable, django_script.__file__, str(cr.request_id)],
#                                       env=os.environ)
            # 在windows上使用Popen,会和socket冲突,
            # 所以在windows平台使用wait方法,等待子进程结束.
            # 这种情况下不能称之为concurrent program.
            # process.wait()    # 使用多线程服务器时,不需要等待.cherrypy server
        else:
            process = subprocess.Popen([sys.executable, django_script.__file__, str(cr.request_id)], 
                                       close_fds=True,
                                       env=os.environ)
    #os.spawnl(os.P_WAIT, os.environ['SystemRoot'] + "\\system32\\mspaint.exe", "mspaint.exe " )
    #os.system("start " + "\"new cmd window\" " + sys.executable + " " + concurrent.__file__) 


    return cr.request_id


def get_request_summary(request_id):
    pass
    
    # return request summary info 
    return -1


def wait_for_request(request_id):
    
    
    
    
    pass


def stop_request(request_id):
    # get pid by request id
  
    # kill the pid
    
    # update to db
    
    # return false when fail
    pass



