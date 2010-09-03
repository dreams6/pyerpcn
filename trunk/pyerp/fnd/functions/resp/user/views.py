# -*- coding: utf-8 -*- 
from django.core.paginator import Paginator

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

####################
# 可显示项目
####################



####################
# 查询
####################
def query(request):
    from django.utils import simplejson
    
    try:
        page_num = int(request.GET.get('page', '1'))
    except ValueError:
        page_num = 1
    
    paginator = Paginator(User.objects.all(), 20)
    context = {
        'app_path': request.get_full_path(), 
        'page': paginator.page(page_num),
        'filter_properties' : simplejson.dumps(properties),
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
