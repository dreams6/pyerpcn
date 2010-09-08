# -*- coding: utf-8 -*- 

import urllib

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.utils.version import get_svn_revision, get_version
from pyerp.fnd.models import User


__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)

####################
# 过滤器属性
####################
properties = {
      'status'      : { 'type': 'radio', 'label': '状态' , 'options': ['accepted',
                                                                'assigned',
                                                                'closed',
                                                                'new',
                                                                'reopened'] },
      'due_date'    : { 'type': 'text', 'label': '预计完成日期' },
      'due_hours'   : { 'type': 'text', 'label': '预计工时' },
      'description' : { 'type': 'textarea', 'label': '描述' },
      'reporter'    : { 'type': 'text', 'label': '提交者' },
      'cc'          : { 'type': 'text', 'label': '抄送' },
      'resolution'  : { 'type': 'radio', 'label': '解决状态', 'options': ['不需要解决',
                                                               '解决-未满足期待',
                                                               '解决-满足期待',
                                                               '解决-超出期待'
                                                              ] },
      'actual_hours': { 'type': 'text', 'label': '实际工时' },
      'component'   : { 'type': 'select', 'label': '组件', 'options': ['pyerp.ap',
                                                            'pyerp.ar',
                                                            'pyerp.fnd',
                                                            'pyerp.gl' ] },
      'summary'     : { 'type': 'text', 'label': '概要' },
      'priority'    : { 'type': 'select', 'label': '优先度', 'options': ['最高优先级',
                                                            '高优先级',
                                                            '中等优先级',
                                                            '低优先级',
                                                            '最低优先级' ] },
      'keywords'    : { 'type': 'text', 'label': '关键词'},
      'version'     : { 'type': 'select', 'label': '版本', 'options': ['0.0.2-dev-0',
                                                          '0.0.1-dev-0',
                                                          '0.1.0-alpha']},
      'milestone'   : { 'type': 'select', 'label': '里程碑', 'options': ['01_Pilot',
                                                              '02_基础应用程序集',
                                                              '03_财务应用程序集',
                                                              '04_结合测试' ] },
      'owner'       : { 'type': 'text', 'label': '所有者' },
      'type'        : { 'type': 'select', 'label': '类型', 'options': ['任务',
                                                      '缺陷',
                                                      '功能增强'] },
      'actual_date' : { 'type': 'text', 'label': '实际完成日期' }
}

modes = {'text'     : [{'text': '包含',  'value': '~'},
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
columns = [{'text': '概要',   'value': 'summary'},
           {'text': '状态',   'value': 'status'},
           {'text': '所有者',   'value': 'owner'},
           {'text': '优先度',   'value': 'priority'},
           {'text': '里程碑',   'value': 'milestone'},
           {'text': '组件',   'value': 'component'},
           {'text': '版本',   'value': 'version'},
           {'text': '解决状态',   'value': 'resolution'},
           {'text': '预计工时',   'value': 'due_hours'},
           {'text': '预计完成日期',   'value': 'due_date'},
           {'text': '实际工时',   'value': 'actual_hours'},
           {'text': '预计工时',   'value': 'due_hours'},
           {'text': '实际完成日期',   'value': 'actual_date'},
           {'text': '提交者',   'value': 'reporter'},
           {'text': '关键词',   'value': 'keywords'},
           {'text': '抄送',   'value': 'cc'},
           {'text': '创建时间',   'value': 'time'},
           {'text': '修改时间',   'value': 'changetime'},
           ]

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
            pv = request.REQUEST.getlist(prop_name)
            req_params[prop_name] = pv
        ####################
        # 操作符
        ####################
        if request.REQUEST.has_key(prop_name + '_mode'):
            pv = request.REQUEST.getlist(prop_name + '_mode')
            req_params[prop_name + '_mode'] = pv
    
    ####################
    # 一页显示数量
    ####################
    if request.REQUEST.has_key('max'):
        req_params['max'] = request.REQUEST['max']
        
    ##############################
    # 请求参数为空时，设定缺省参数
    ##############################
    if not req_params:
        req_params['max'] = '20'
        
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
        'selected_columns' : ['cc'],
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
