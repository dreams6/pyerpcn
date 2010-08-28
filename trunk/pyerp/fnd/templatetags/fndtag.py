# -*- coding: utf-8 -*- 

from django.template import Library
from django.utils.safestring import mark_safe
from django.db.models import Q as Q
from django.conf import settings
from django.utils.translation import ugettext as _

from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.sites import respsite, usersite, pubsite
from pyerp.fnd.models import Responsibility, MenuItem
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)

register = Library()

def fnd_show_resp(resp_id):
    """

    """

    menu_html_str = """
    <table width="100%" border="0" cellspacing="0" cellpadding="0">
    """
    responsibilities = fnd_global.user.responsibilities.all()
    
    for responsibility in responsibilities:
        if resp_id is not None and responsibility.id==int(resp_id):
            l_class = "mlinkselected" 
        else: 
            l_class = "mlink" 
        menu_html_str = menu_html_str + ("""<tr>
    <td><img src="%simages/t.gif" width="4"></td>
    <td vAlign="top"><a href="%smain/%s/"><img height="16" src="%simages/resp_folder.gif" width="16" border="0"></a></td>
    <td><img src="%simages/t.gif" width="4"></td>
    <td width="100%%"><a class="%s" href="%smain/%s/">%s</a></td>
  </tr>
  """ % (fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, 
         fnd_global.context_prefix + settings.FND_USER_SITE_PREFIX, 
         responsibility.id, 
         fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, 
         fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, 
         l_class, 
         fnd_global.context_prefix + settings.FND_USER_SITE_PREFIX, 
         responsibility.id, 
         _(responsibility.name)) )
    menu_html_str = menu_html_str + "</table>"
    return mark_safe(menu_html_str)
fnd_show_resp = register.simple_tag(fnd_show_resp)


def r_menuitem_html(p_menu, p_title, resp, sub_title=None):

    ret = ""
    # functions
    mi_list = MenuItem.objects.filter(p_menu=p_menu, function__isnull=False).order_by('seq')
    if mi_list and sub_title:
        ret = ret + sub_title
    for mi in mi_list:
        ret = ret + ("""<tr>
  <td><img src="%simages/t.gif" width="4"></td>
  <td valign="top"><a target="_blank" href="%s"><img src="%simages/func_item.gif" border="0"></a></td>
  <td><img src="%simages/t.gif" width="4"></td>
  <td width="100%%"><a class="mlink" href="%s">%s</a></td>
</tr>""" % (fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, 
            fnd_global.context_prefix + settings.FND_RESP_SITE_PREFIX + str(resp.id) + "/" + str(mi.id) + "/" + str(mi.function.id) + "/" + (mi.function.paramters or ""), 
            fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, 
            fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, 
            fnd_global.context_prefix + settings.FND_RESP_SITE_PREFIX + str(resp.id) + "/" + str(mi.id) + "/" + str(mi.function.id) + "/" + (mi.function.paramters or ""), 
            _(mi.prompt)) )
    
    # submenus
    mi_list = MenuItem.objects.filter(p_menu=p_menu, submenu__isnull=False).order_by('seq')
    for mi in mi_list:
        sub_t = ("""<tr>
  <td colspan="4"><img height="10" src="%simages/t.gif"></td>
</tr>
<tr>
  <td><img src="%simages/t.gif" width="4"></td>
  <td colspan="3"><span class="mtitle">%s</span></td>
</tr>""" % (fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, 
            fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, 
            (p_title and p_title + " : ") + _(mi.prompt) ) )
        ret = ret + r_menuitem_html(mi.submenu, _(mi.prompt), resp, sub_t)

    return ret

def fnd_show_resp_menu(resp_id):
    """

    """
    menu_html_str = """<table width="100%" border="0" cellspacing="0" cellpadding="0">"""
    if resp_id is None:
        menu_html_str = menu_html_str + ("""<tr><td><img src="%simages/t.gif" width="4"></td><td colspan="3" width="100%%"><span class="mtitle">%s</span></td></tr>""" 
                                         % (fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, '请选择职责.'))
    else:
        try:
            resp = fnd_global.user.responsibilities.get(pk=resp_id)
            menu_html_str = menu_html_str + ("""<tr><td><img src="%simages/t.gif" width="4"></td><td colspan="3"><span class="mtitle">%s</span></td></tr>""" 
                                             % (fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, _(resp.name)))
            menu_html_str = menu_html_str + r_menuitem_html(resp.menu, "", resp)
        except (Responsibility.DoesNotExist):
        # 职责不存在或,用户不能访问
            menu_html_str = menu_html_str + ("""<tr><td><img src="%simages/t.gif" width="4"></td><td colspan="3" width="100%%"><span class="mtitle">%s</span></td></tr>""" 
                                             % (fnd_global.context_prefix + settings.FND_MEDIA_PREFIX, '不可访问的职责.'))


    menu_html_str = menu_html_str + ("""<tr><td colspan="4"><img height="10" src="%simages/t.gif"></td></tr></table>""" 
                                         % (fnd_global.context_prefix + settings.FND_MEDIA_PREFIX))
    return mark_safe(menu_html_str)

fnd_show_resp_menu = register.simple_tag(fnd_show_resp_menu)



