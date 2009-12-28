# -*- coding: utf-8 -*- 


from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django import forms
from django.db.models import Q as Q

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.models import Menu, MenuItem, Function
from pyerp.fnd.gbl import fnd_global


def index(request):
    try:
        page_num = int(request.GET.get('page', '1'))
    except ValueError:
        page_num = 1

    paginator = Paginator(Menu.objects.all(), 20)
    context = {
        'app_path': request.get_full_path(), 
        'page': paginator.page(page_num),
    }
    return fnd_render_to_response('resp/menu/index.html', context)

def add(request):
    context = {
        'app_path': request.get_full_path(), 
    }
    return fnd_render_to_response('resp/menu/add.html', context)


def edit(request, f_id=None):
    """
    TODO return json data
    """
    from django.utils import simplejson
    from django.http import HttpResponse
    from django.conf import settings

    if request.is_ajax() and f_id is not None:
        def menu_to_dict(m):
            return {"status" : "query",
                    "data" : { "id" : m.id, 
                               "name" : m.name,
                               "description" : m.description,
                               "last_updated_by"  : m.last_updated_by,
                               "last_updated_date" :  m.last_updated_date.strftime("%Y-%m"),
                              }
                    }

        def menuitem_to_dict(mi):
            return {"status" : "query",
                    "data" : { "id" : mi.id,
                               "seq" : mi.seq,
                               "prompt" : mi.prompt,
                               "submenu"     : mi.submenu and mi.submenu.name,
                               "func"        : mi.function and mi.function.name,
                               "description" :  mi.description,
                               "last_updated_by" :  mi.last_updated_by,
                               "last_updated_date" :  mi.last_updated_date.strftime("%Y-%m"),
                              }
                    }
        
        menu = Menu.objects.get(pk=f_id)
        menuitems = MenuItem.objects.filter(Q(p_menu=menu))
        
        ret_json = {"head" : {"status"  : "200",
                              "message" : {"menu"      : [],
                                           "menuitems" : []}},
                    "body" : {
                              "status"    : "query",
                              "menu"      : menu_to_dict(menu),
                              "menuitems" : [menuitem_to_dict(menu_item) for menu_item in menuitems]
                              }
                    }

        if settings.DEBUG and request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            from django.db import connection
            ret_json['head']['sql_queries'] = connection.queries
        

        json = simplejson.dumps(ret_json)
        return HttpResponse(json, mimetype='application/json')

    context = {
        'app_path': request.get_full_path(),
        'f_id' : f_id,
    }
    return fnd_render_to_response('resp/menu/add.html', context)

#===============================================

def submenu_sug(request, m_id=None):
    from django.utils import simplejson
    from django.http import HttpResponse
    from django.db.models import Q
    req_data = request.REQUEST.get("req_data")
    page_num = int(request.GET.get('page', '1'))
    if m_id is not None:
        paginator = Paginator(Menu.objects.exclude(Q(pk=m_id)).filter(Q(name__startswith=req_data)), 10)
    else:
        paginator = Paginator(Menu.objects.filter(Q(name__startswith=req_data)), 10)
    page =  paginator.page(page_num)
    response = {'has_previous': page.has_previous(),
                'has_next': page.has_next(),
                'page_number' : page.number,
                'num_pages' : page.paginator.num_pages,
                'object_list': [[record.name, str(record.id)] for record in page.object_list],
                }
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype='application/json')

def func_sug(request):
    from django.utils import simplejson
    from django.http import HttpResponse
    from django.db.models import Q
    req_data = request.REQUEST.get("req_data")
    page_num = int(request.GET.get('page', '1'))
    paginator = Paginator(Function.objects.filter(Q(name__startswith=req_data)), 10)
    page =  paginator.page(page_num)
    response = {'has_previous': page.has_previous(),
                'has_next': page.has_next(),
                'page_number' : page.number,
                'num_pages' : page.paginator.num_pages,
                'object_list': [[record.name] for record in page.object_list],
                }
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype='application/json')




def validate_menu_id(value):
    if not value:
        return {'code' : '', 'content' : '主键-非显示必须输入.', 'src' : 'id'}
 
def validate_menu_name(value):
    if not value:
        return {'code' : '', 'content' : '菜单名必须输入.', 'src' : 'name'}
    
    if len(value) > 100:
        return {'code' : '', 'content' : '最大长度100位,请输入100位以下的菜单名.', 'src' : 'name'}
 
 
def validate_menu_description(value):
    if not value:
        return {'code' : '', 'content' : '描述必须输入.', 'src' : 'description'}

    if len(value) > 255:
        return {'code' : '', 'content' : '最大长度255位,请输入255位以下的描述.', 'src' : 'description'}


def validate_menuitems_id(value):
    if not value:
        return {'code' : '', 'content' : '主键-非显示必须输入.', 'src' : 'id'}

def validate_menuitems_seq(value):
    if not value:
        return {'code' : '', 'content' : '显示顺序必须输入.', 'src' : 'seq'}
    
    # 数字TODO
    
 
def validate_menuitems_prompt(value):
    if not value:
        return {'code' : '', 'content' : '提示必须输入.', 'src' : 'prompt'}

    if len(value)>100:
        return {'code' : '', 'content' : '最大长度100位,请输入100位以下的提示.', 'src' : 'prompt'}

def validate_menuitems_submenu(value):
    pass
    # 存在check TODO
 
 
def validate_menuitems_func(value):
    if not value:
        return {'code' : '', 'content' : '功能部件必须输入.', 'src' : 'func'}
    
    pass
    # 存在check TODO


def validate_menuitems_description(value):

    if len(value) > 255:
        return {'code' : '', 'content' : '最大长度255位,请输入255位以下的描述.', 'src' : 'description'}


def validate_menu(record):
    ret = []
    data = record['data']
#    _id_v_ret = validate_menu_name(data['id'])
#    if _id_v_ret:
#        ret.append(_id_v_ret)
    _name_v_ret = validate_menu_name(data['name'])
    if _name_v_ret:
        ret.append(_name_v_ret)
    _description_v_ret = validate_menu_name(data['description'])
    if _description_v_ret:
        ret.append(_description_v_ret)
    return ret

def validate_menuitems_row(record):
    ret = []
    data = record['data']
#    _id_v_ret = validate_menuitems_id(data['id'])
#    if _id_v_ret:
#        ret.append(_id_v_ret)

    _seq_v_ret = validate_menuitems_seq(data['seq'])
    if _seq_v_ret:
        ret.append(_seq_v_ret)
    _prompt_v_ret = validate_menuitems_prompt(data['prompt'])
    if _prompt_v_ret:
        ret.append(_prompt_v_ret)
        
    if data['submenu'] and data['func']:
        ret.append({'code' : '', 'content' : '子菜单或功能部件只能输入其中一个.', 'src' : 'description'})
    else:
        
        _submenu_v_ret = validate_menuitems_submenu(data['submenu'])
        if _submenu_v_ret:
            ret.append(_submenu_v_ret)
        _func_v_ret = validate_menuitems_func(data['func'])
        if _func_v_ret:
            ret.append(_func_v_ret)
    _description_v_ret = validate_menuitems_description(data['description'])
    if _description_v_ret:
        ret.append(_description_v_ret)
    return ret

def validate_menuitems(records):
    ret = []
    has_err = False
    for record in records:
        r_ret = validate_menuitems_row(record)
        if r_ret:
            ret.append(r_ret)
            has_err = True
        else:
            ret.append([])
    if (has_err):
        return ret
    else:
        return []

def validate(body):
    _error_msg = {}
    _menu_v_ret = validate_menu(body['menu'])
    _menuitems_v_ret = validate_menuitems(body['menuitems'])

    return {"menu" : _menu_v_ret or [],  "menuitems" : _menuitems_v_ret or []}


#
# 正常时返回None.
# return message when error.
#
def save_db(body):
    record = body['menu']
    if record['status']=="insert":
        m = menu_Model()
        m.id = record['data']['id'] 
        m.name = record['data']['name'] 
        m.description = record['data']['description'] 
        model.save()

    elif record['status']=="change":
        m = menu_Model.objects.get(pk=record['data']['id'])
        m.id = record['data']['id'] 
        m.name = record['data']['name'] 
        m.description = record['data']['description'] 
        model.save()

    for record in body['menuitems']:
        if record['status']=="insert":
            m = menuitems_Model()
            m.id = record['data'].id
            m.seq = record['data'].seq
            m.prompt = record['data'].prompt
            m.submenu = record['data'].submenu
            m.func = record['data'].func
            m.description = record['data'].description
            m.save()

        elif record['status']=="change":
            m = menuitems_Model.objects.get(pk=record['data']['id'])
            m.id = record['data'].id
            m.seq = record['data'].seq
            m.prompt = record['data'].prompt
            m.submenu = record['data'].submenu
            m.func = record['data'].func
            m.description = record['data'].description
            m.save()

        elif record['status']=="delete":
            m = menuitems_Model.objects.get(pk=record['data']['id'])
            m.delete()

#
# 保存画面上编辑的数据.
#
#
def save(request):
    from django.utils import simplejson
    from django.http import HttpResponse
    json_request = simplejson.loads(request.raw_post_data)
    json_request['head']['message'] = json_request['head'].has_key('message') and json_request['head']['message'] or {}
    json_body = json_request.has_key('body') and json_request['body'] or {}
    _v_ret = validate(json_body)
    json_request['head']['message'] = _v_ret
    if _v_ret['menu'] or _v_ret['menuitems']:
        json = simplejson.dumps(json_request)
        return HttpResponse(json, mimetype='application/json')
    # if no err in input save the body to db
    save_db(json_body)
    json = simplejson.dumps(json_request)
    return HttpResponse(json, mimetype='application/json')

