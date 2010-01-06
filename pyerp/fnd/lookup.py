# -*- coding: utf-8 -*- 

from models import LookUpNode
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)



# LookUpNode===============================================================

#
# 
# 
#
def lookupmeaning(**arg):
  """\
    Arguments:
      id     - 
      path - 
      name   - \
  """
  if arg.has_key("id"):
    parent_node = LookUpNode.objects.get(pk=arg['id'])
    if arg.has_key("name"):
      node = LookUpNode.objects.get(parent_node=parent_node, name=arg['name'])
      return node.meaning
    else:
      return parent_node.meaning
  elif arg.has_key("path"):
    parent_node = LookUpNode.objects.get(node_path=arg['path'])
    if arg.has_key("name"):
      node = LookUpNode.objects.get(parent_node=parent_node, name=arg['name'])
      return node.meaning
    else:
      return parent_node.meaning
  return None

#
# 
# 
#
def lookuplist(**arg):
  """
  
  """
  if arg.has_key("id"):
    if arg['id'] is None:
      if arg.has_key("leaf"):
        return LookUpNode.objects.filter(parent_node__isnull=True, leaf_node=arg['leaf']).order_by('id')
      else:
        return LookUpNode.objects.filter(parent_node__isnull=True).order_by('id')
    else:
      parent_node = LookUpNode.objects.get(pk=arg['id'])
      if arg.has_key("leaf"):
        return LookUpNode.objects.filter(parent_node=parent_node, leaf_node=arg['leaf']).order_by('id')
      else:
        return LookUpNode.objects.filter(parent_node=parent_node).order_by('id')
  elif arg.has_key("path"):
    if arg['path'] is None:
      return None
    elif arg['path']=="/":
      if arg.has_key("leaf"):
        return LookUpNode.objects.filter(parent_node__isnull=True, leaf_node=arg['leaf']).order_by('id')
      else:
        return LookUpNode.objects.filter(parent_node__isnull=True).order_by('id')
    else:
      parent_node = LookUpNode.objects.get(node_path=arg['path'])
      if arg.has_key("leaf"):
        return LookUpNode.objects.filter(parent_node=parent_node, leaf_node=arg['leaf']).order_by('id')
      else:
        return LookUpNode.objects.filter(parent_node=parent_node).order_by('id')
  return None
  # return a list of parentnode or lookuppath

#
# 
# 
#
def add(name, 
        meaning, 
        description=None, 
        parentnodeid=None, 
        leaf_node=False):

  node = LookUpNode()
  node.name = name
  node.meaning = meaning
  node.description = description
  node.leaf_node = leaf_node
  node.name = name
  if parentnodeid!=None:
    parent_node = LookUpNode.objects.get(pk=parentnodeid)
    node.parent_node = parent_node
    node.node_path = parent_node.node_path + "/" + name
  else:
    node.node_path = "/" + name

  node.enabled = True

  # ==============================
  node.created_by = fnd_global.user_id
  node.last_updated_by = fnd_global.user_id
  # ==============================
  node.save()
  return node

#
# 
# 
#
def init_lookup():
    node = addlookupnode("MSG_TYPE", "Message Type")
    add("E", "Error", "Error.", node.id)
    add("W", "Warning", "Warning.", node.id)
    add("N", "Note", "Note.", node.id)
    add("Q", "Question", "Question.", node.id)
    add("H", "Hint", "Hint.", node.id)
    add("T", "Tip", "Tip.", node.id)
    add("P", "Prompt", "Prompt.", node.id)
    add("M", "Menu", "Menu.", node.id)
    add("O", "Other", "Other.", node.id)
    
    node = addlookupnode("MSG_CATEGORY", "Message Category")
    add("SYS", "System", "System.", node.id)
    add("USR", "User", "User.", node.id)
    add("PRO", "Product", "Product.", node.id)
    add("ERR", "Error", "Error.", node.id)
    add("SEC", "Security", "Security.", node.id)
    add("APP", "Application", "Application.", node.id)
    
    pass

# MessageText===============================================================


#
# 
# 
#
