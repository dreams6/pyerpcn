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



####################
# 查询比较方法
####################
def get_modes():
    modes = {'text'     : [{'text': _('contains'),         'value': '~'},
                           {'text': _('doesn\'t contain'), 'value': '!~'},
                           {'text': _('begins with'),      'value': '^'},
                           {'text': _('ends with'),        'value': '$'},
                           {'text': _('equal'),            'value': ''},
                           {'text': _('not equal'),        'value': '!'}],
             'select'   : [{'text': _('equal'),            'value': ''},
                           {'text': _('not equal'),        'value': '!'}],
             'textarea' : [{'text': _('contains'),         'value': '~'},
                           {'text': _('doesn\'t contain'), 'value': '!~'}]
            }
    return modes

####################
# 过滤器属性
####################
def get_filter_properties():
    
    def y_options():
        return ['none', 'days', 'accesses']
    
    
    properties = {
          'username'    : { 'type': 'text',   'label': _('Username') },
          'email'       : { 'type': 'text',   'label': _('Email address') },
          'pwd_expiration_type' : { 'type': 'radio',   'label': _('Password expirtion') , 'options' : y_options()},
          'first_name'  : { 'type': 'text',   'label': _('last name') },
          'last_name'   : { 'type': 'text',   'label': _('first name') },
          'description' : { 'type': 'text',   'label': _('Description') },
          'type'        : { 'type': 'select', 'label': '类型', 'options': [u'任务',
                                                                           u'缺陷',
                                                                           u'功能增强'] },
    }
    return properties

####################
# 可显示项目
####################
def get_columns():
    columns = [{'text': _('Username'),            'value': 'username'},
               {'text': _('Email address'),       'value': 'email'},
               {'text': _('Password expirtion'),  'value': 'pwd_expiration_type'},
               {'text': _('last name'),           'value': 'first_name'},
               {'text': _('first name'),          'value': 'last_name'},
               {'text': _('Description'),         'value': 'description'}]
    return columns

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
    url = urllib.urlencode(req_params)
    return url and url + '&' or ''

######################
# 将请求参数转换成字典
######################
def req2dict(request, properties):
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
    
    ####################
    # 过滤器属性
    ####################
    properties = get_filter_properties()
    ######################
    # 将请求参数转换成字典
    ######################
    req_params = req2dict(request, properties)
    
    ############################
    # 将请求重镜像成带参数的GET请求
    ############################
    redirect_url = query_string(req_params)
    if 'update' in request.REQUEST:
        return HttpResponseRedirect('?' + redirect_url)

    ######################################
    # 请求参数为空时(初始显示时)，设定缺省参数
    ######################################
    #~ if not req_params:
        #~ req_params['max'] = '20'

    try:
        page_num = int(request.REQUEST.get('page', '1'))
    except ValueError:
        page_num = 1

    paginator = Paginator(User.objects.all(), 2)

    modes = get_modes()
    columns = get_columns()

    context = {
        'app_path': request.get_full_path(), 
        'page': paginator.page(page_num),
        'filter_properties' : get_filter_properties(),
        'filter_properties_json' : simplejson.dumps(properties),
        'filter_modes' : get_modes(),
        'filter_modes_json' : simplejson.dumps(modes),
        'filter_columns' : columns,
        'req_params' : req_params,
        'link_url' : redirect_url,
        
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
