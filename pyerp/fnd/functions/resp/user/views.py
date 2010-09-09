# -*- coding: utf-8 -*- 

import urllib

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.utils.version import get_svn_revision, get_version
from pyerp.fnd.models import User


__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


def y_options():
    
    
    
    return ['none', 'days', 'accesses']


####################
# 过滤器属性
####################
properties = {
      'username'    : { 'type': 'text',   'label': '用户名' },
      'email'       : { 'type': 'text',   'label': '电子邮件' },
      'pwd_expire_type' : { 'type': 'radio',   'label': '密码过期类型' , 'options' : y_options()},
      'first_name'  : { 'type': 'text',   'label': '姓' },
      'last_name'   : { 'type': 'text',   'label': '名' },
      'description' : { 'type': 'text',   'label': '描述' },
      'type'        : { 'type': 'select', 'label': '类型', 'options': [u'任务',
                                                                       u'缺陷',
                                                                       u'功能增强'] },
}

modes = {'text'     : [{'text': '包含',   'value': '~'},
                       {'text': '不包含', 'value': '!~'},
                       {'text': '开始以', 'value': '^'},
                       {'text': '结束以', 'value': '$'},
                       {'text': '等于',   'value': ''},
                       {'text': '不等于', 'value': '!'}],
         'select'   : [{'text': '等于',   'value': ''},
                       {'text': '不等于', 'value': '!'}],
         'textarea' : [{'text': '包含',   'value': '~'},
                       {'text': '不包含', 'value': '!~'}]
        }

####################
# 可显示项目
####################
columns = [{'text': '用户名',         'value': 'username'},
           {'text': '电子邮件',       'value': 'email'},
           {'text': '密码过期类型',   'value': 'pwd_expire_type'},
           {'text': '姓',             'value': 'first_name'},
           {'text': '名',             'value': 'last_name'},
           {'text': '描述',           'value': 'description'}]

###############################
# 将请求参数字典转换成query url
###############################
def query_string(req_dict):
    req_params = []
    for param_name, param_value in req_dict.items():
        if (type(param_value)==list):
            for v in param_value:
                req_params.append( (param_name, v.encode('utf-8')) )
        else:
            req_params.append( (param_name, param_value.encode('utf-8')) )
    return urllib.urlencode(req_params)

######################
# 将请求参数转换成字典
######################
def req2dict(request):
    req_params = {}
    for prop_name in properties.keys():
        ####################
        # 指定的过滤条件
        ####################
        if request.REQUEST.has_key(prop_name):
            req_params[prop_name] = request.REQUEST.getlist(prop_name)
        ####################
        # 操作符
        ####################
        if request.REQUEST.has_key(prop_name + '_mode'):
            req_params[prop_name + '_mode'] = request.REQUEST.getlist(prop_name + '_mode')
    ####################
    # 显示列名
    ####################
    if request.REQUEST.has_key('col'):
        req_params['col'] = request.REQUEST.getlist('col')
    ####################
    # 一页显示数量
    ####################
    if request.REQUEST.has_key('max'):
        req_params['max'] = request.REQUEST['max']
    #~ ##############################
    #~ # 请求参数为空时，设定缺省参数
    #~ ##############################
    #~ if not req_params:
        #~ req_params['max'] = '20'
    return req_params

####################
# 查询
####################
def query(request):
    from django.utils import simplejson

    req_params = req2dict(request)
    
    if 'update' in request.REQUEST:
        redirect_url = query_string(req_params)
        return HttpResponseRedirect('?' + redirect_url)

    ######################################
    # 请求参数为空时(初始显示时)，设定初始参数
    ######################################
    #~ if not req_params:
        #~ req_params['max'] = '20'


    try:
        page_num = int(request.GET.get('page', '1'))
    except ValueError:
        page_num = 1

    paginator = Paginator(User.objects.all(), 20)
    context = {
        'app_path': request.get_full_path(), 
        'page': paginator.page(page_num),
        'filter_properties' : properties,
        'selected_filter_properties' : ['status', 'owner', 'priority'],
        'filter_properties_json' : simplejson.dumps(properties),
        'filter_modes' : modes,
        'filter_modes_json' : simplejson.dumps(modes),
        'filter_columns' : columns,
        'req_params' : req_params,
        
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
