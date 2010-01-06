# -*- coding: utf-8 -*- 
from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd import models as fnd_models
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)



def index(request):
    context = {
        'app_path': request.get_full_path(),
    }
    
    return fnd_render_to_response('resp/executable/index.html', context)

def index_load(request):
    from django.utils import simplejson
    from django.http import HttpResponse
    
    if request.is_ajax():
        exec_list = fnd_models.ConcurrentExecutable.objects.all()
        def exec_to_dict(m):
            return {"status" : "query",
                    "data" : { "executable_id" : m.executable_id, 
                               "name" : m.name,
                               "method" : m.method,
                               "file"  : m.file,
                               "execution_path" :  m.execution_path,
                              }
                    }
        ret_json = {"head" : {"status"  : "200",
                              "message" : {"executables" : []}},
                    "body" : {
                              "status"    : "query",
                              "executables" : [exec_to_dict(exec_item) for exec_item in exec_list]
                              }
                    }
        json = simplejson.dumps(ret_json)
        return HttpResponse(json, mimetype='application/json')


