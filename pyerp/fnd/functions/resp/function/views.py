# -*- coding: utf-8 -*- 
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django import forms

from pyerp.fnd.models import Function
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)



class FunctionForm(forms.ModelForm):
    id                 = forms.IntegerField(widget=forms.HiddenInput, required=False)
    name               = forms.CharField(max_length=30)
    description        = forms.CharField(max_length=255,widget=forms.Textarea(attrs={'size':'60','rows':'6',"autocomplete":"off"}))
    package            = forms.CharField(max_length=255)
    paramters          = forms.CharField(max_length=255)
#    type = forms.IntegerField(widget=forms.Select(choices=s_models.QUESTION_TYPES))
#
    class Meta:
        model = Function
#    def clean(self):
#        from django.forms.util import ErrorList
#        cleaned_data = self.cleaned_data
#        l_content = cleaned_data.get("content")
#        l_type = cleaned_data.get("type")
#        return cleaned_data



def index(request):
    try:
        page_num = int(request.GET.get('page', '1'))
    except ValueError:
        page_num = 1

    paginator = Paginator(Function.objects.all(), 20)
    context = {
        'app_path': request.get_full_path(), 
        'page': paginator.page(page_num),
    }

    return fnd_render_to_response('resp/function/index.html', context)

def add(request):
    form = FunctionForm()
    if request.method == 'POST' and request.POST.get("_save"):
        form = FunctionForm(request.POST)
        func = Function()
        func.name = form['name'].data
        func.description = form['description'].data
        func.package = form['package'].data
        func.paramters = form['paramters'].data
        # ---------------------------------------
        func.created_by = fnd_global.user_id
        func.last_updated_by = fnd_global.user_id
        func.save()
        return HttpResponseRedirect('../')
        
    context = {
        'app_path': request.get_full_path(), 
        'form': form,
    }
    return fnd_render_to_response('resp/function/add.html', context)


def edit(request, f_id):
    
    func = Function.objects.get(pk=f_id)
    if request.method == 'POST' and request.POST.get("_save"):
        form = FunctionForm(request.POST, instance=func)
        func.name = form['name'].data
        func.description = form['description'].data
        func.package = form['package'].data
        func.paramters = form['paramters'].data
        # ---------------------------------------
        func.created_by = fnd_global.user_id
        func.last_updated_by = fnd_global.user_id
        func.save()
        return HttpResponseRedirect('../')
    form = FunctionForm(instance=func)
    context = {
        'app_path': request.get_full_path(),
        'form': form,
    }
    return fnd_render_to_response('resp/function/add.html', context)

def save(request):
    
    
    pass


#
#
#
def func_list():
    """
    取得func列表 for sugest
    """
    from django.conf import settings
    import types
    import os
    def can_import(package):
        try:
            return True
        except ImportError:
            return False
    for app in settings.INSTALLED_APPS:
        # Step 1: find out the functions module
        try:
            app_funcs_mod = __import__(app + '.functions', {}, {}, [''])
        except ImportError:
            continue

        # Step 2: find out the function from functions module
        for label in ('pub', 'user', 'resp'):
            try:
                app_func_label_path = __import__(app_funcs_mod.__name__ + '.' + label, {}, {}, ['']).__path__[0]
                for f in os.listdir(app_func_label_path):
                    if not f.startswith('.') and os.path.isdir(os.path.join(app_func_label_path, f)):
                        try:
                            app_func_mod = __import__(app_funcs_mod.__name__ + '.' + label + '.' + f, {}, {}, ['urls', 'views'])
                            if not hasattr(app_func_mod, 'urls'):
                                continue
                            if hasattr(app_func_mod, 'get_version'):
                                pass
                            yield (app, label, app_func_mod.__name__ , app_func_mod.__version__)
                        except:
                            pass
            except:
                pass
#
#
#
def func_sug(request):
    
    from django.utils import simplejson
    from django.http import HttpResponse
    from django.db.models import Q
    from pyerp.ak.models import Postal
    req_data = request.REQUEST.get("req_data")
    page_num = int(request.GET.get('page', '1'))

    filter_list = [record for record in func_list() if record[2].startswith(req_data)]
    
    paginator = Paginator(filter_list, 10)

    page =  paginator.page(page_num)
    response = {'has_previous': page.has_previous(),
                'has_next': page.has_next(),
                'page_number' : page.number,
                'num_pages' : page.paginator.num_pages,
                'object_list': [[record[2],record[0], record[1]] for record in page.object_list],
                }
    json = simplejson.dumps(response)
    return HttpResponse(json, mimetype='application/json')



