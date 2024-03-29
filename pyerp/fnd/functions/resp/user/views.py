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
    modes = {'text'     : ( ('~'  ,   _('contains')           ),
                            ('!~' ,   _('doesn\'t contain')   ),
                            ('^'  ,   _('begins with')        ),
                            ('$'  ,   _('ends with')          ),
                            (''   ,   _('equal')              ),
                            ('!'  ,   _('not equal')          ) ),
             'select'   : ( (''   ,   _('equal')              ),
                            ('!'  ,   _('not equal')          ) ),
             'textarea' : ( ('~'  ,   _('contains')           ),
                            ('!~' ,   _('doesn\'t contain')   ) )
            }
    return modes

####################
# 过滤器属性
####################
def get_filter_properties():
    properties = {
          'username'    : { 'type': 'text',   'label': _('Username') },
          'email'       : { 'type': 'text',   'label': _('Email address') },
          'pwd_expiration_type' : 
                          { 'type': 'radio',   'label': _('Password expirtion') , 
                            'options' : ( ('0', 'none'), 
                                          ('1', 'days'),
                                          ('2', 'accesses'))},
          'first_name'  : { 'type': 'text',   'label': _('last name') },
          'last_name'   : { 'type': 'text',   'label': _('first name') },
          'description' : { 'type': 'text',   'label': _('Description') },
          'type'        : { 'type': 'select', 'label': '类型', 
                            'options' : ( ('1', '任务'),
                                          ('2', '缺陷'),
                                          ('3', '功能增强')) },
    }
    return properties

####################
# 可显示项目
####################
def get_columns():
    columns = ( ('username',            _('Username')             ),
                ('email',               _('Email address')        ),
                ('pwd_expiration_type', _('Password expirtion')   ),
                ('first_name',          _('last name')            ),
                ('last_name',           _('first name')           ),
                ('description',         _('Description')          ) )
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
    # 一页显示数量/x页
    ####################
    if request.REQUEST.has_key('max'):
        req_params['max'] = request.REQUEST.get('max', '20')
    if request.REQUEST.has_key('page'):
        req_params['page'] = request.REQUEST.get('page', '1')
    
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
    from django.contrib import messages
    
    ####################
    # 过滤器属性
    ####################
    properties = get_filter_properties()
    ######################
    # 将请求参数转换成字典
    ######################
    req_params = req2dict(request, properties)
    
    ######################################
    # 请求参数为空时(初始显示时)，设定缺省参数
    ######################################
    if not req_params:
        req_params['max'] = '20'
        req_params['col'] = ['username', 'email', 'pwd_expiration_type', 'first_name', 'last_name', 'description']
        req_params['page'] = '1'
    
    ############################
    # 将请求重镜像成带参数的GET请求
    ############################
    redirect_url = query_string(req_params)
    if 'update' in request.REQUEST:
        return HttpResponseRedirect('?' + redirect_url)
    
    ############################
    # 输入校验
    ############################
    
    
    
    context = {}
    modes = get_modes()
    columns = get_columns()
    context.update({'app_path': request.get_full_path(),
                    'filter_properties' : properties,
                    'filter_properties_json' : simplejson.dumps(properties),
                    'filter_modes' : get_modes(),
                    'filter_modes_json' : simplejson.dumps(modes),
                    'filter_columns' : columns,
                    'req_params' : req_params,
                    'link_url'   : redirect_url} )
    
    messages.warning(request, 'Your account expires in three days.')
    messages.error(request, 'Your account expires in three days.')
    # messages.info(request, 'Your account expires in three days.')
    # messages.debug(request, 'Your account expires in three days.')

    paginator = Paginator(User.objects.all(), 20)
    
    context.update( {'page': paginator.page(int(req_params['page']))} )
    


    return fnd_render_to_response('resp/user/query.html', context, request)

####################
# 添加用户
####################
def add(request):
    context = {
        'app_path': request.get_full_path(),
    }
    return fnd_render_to_response('resp/user/add.html', context)
