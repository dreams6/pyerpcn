# -*- coding: utf-8 -*- 
from django.core.paginator import Paginator

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.utils.version import get_svn_revision, get_version
from pyerp.fnd.models import User


__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)

####################
# 查询
####################
def query(request):
    try:
        page_num = int(request.GET.get('page', '1'))
    except ValueError:
        page_num = 1

    paginator = Paginator(User.objects.all(), 20)
    context = {
        'app_path': request.get_full_path(), 
        'page': paginator.page(page_num),
    }

    return fnd_render_to_response('resp/user/query.html', context)


####################
# 添加用户
####################
def add(request):
    context = {
        'app_path': request.get_full_path(),
    }
    return fnd_render_to_response('resp/user/index.html', context)
