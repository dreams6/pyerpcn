# -*- coding: utf-8 -*- 

from datetime import datetime, date

from django.db import models
from django.utils.encoding import smart_str
from django.contrib.auth import models as dj_auth_models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)

SCHEMA_VERSION = 1

# Create your models here.
class LookUpNode(models.Model):
    name               = models.CharField(max_length=20)
    meaning            = models.CharField(max_length=50)
    description        = models.CharField(max_length=255, null=True)
    leaf_node          = models.BooleanField(default=False)
    parent_node        = models.ForeignKey("self", null=True)
    node_path          = models.CharField(max_length=255, unique=True)
    enabled            = models.BooleanField(null=False, default=True)
    start_date_active  = models.DateField(default=date.today)
    end_date_active    = models.DateField(null=True)
    security_group_id  = models.IntegerField(null=True)
    # ========================================================
    created_by         = models.IntegerField(null=False)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

    class Meta:
        unique_together = (
                ("parent_node", "name"),
                )

MESSAGE_TYPE_CHOICES = (
    ('E', 'Error'),
    ('W', 'Warning'),
    ('N', 'Note'),
    ('Q', 'Question'),
    ('H', 'Hint'),
    ('T', 'Tip'),
    ('P', 'Prompt'),
    ('M', 'Menu'),
    ('O', 'Other'),
)

MESSAGE_CATEGORY_CHOICES = (
    ('SYS', 'System'),
    ('USR', 'User'),
    ('PRO', 'Product'),
    ('ERR', 'Error'),
    ('SEC', 'Security'),
    ('APP', 'Application'),
)

# NEW_MESSAGES
class MessageResource(models.Model):
    #application_id                 not null number
    #message_number                          number(9)
    language_code       = models.CharField(max_length=4)
    name                = models.CharField(max_length=30)
    type                = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)
    text                = models.CharField(max_length=2000)
    description         = models.CharField(max_length=240)
    max_length          = models.IntegerField()
    category            = models.CharField(max_length=10, choices=MESSAGE_CATEGORY_CHOICES)
    severity            = models.CharField(max_length=30)
    log_severity        = models.CharField(max_length=30)

    # ========================================================
    created_by         = models.IntegerField(null=False)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

    class Meta:
        unique_together = (
                ("language_code", "name"),
                )

#
# 
#
VALUESET_LIST_TYPE_CHOICES = (
    ('SLOV', 'List of Values'),
    ('LLOV', 'Long List of Values'),
    ('PLST', 'PopList'),
)
VALUESET_FMT_VALIDATION_TYPE_CHOICES = (
    ('CHAR'     , 'List of Values'),
    ('NUMBER'   , 'Long List of Values'),
    ('DATE'     , 'Long List of Values'),
    ('DATETIME' , 'PopList'),
    ('TIME'     , 'PopList'),
)
VALUESET_VALIDATION_TYPE_CHOICES = (
    ('LOOKUP', 'Lookup'),
    ('RAWSQL', 'rawsql'),
)
class ValueSet(models.Model):
    name                = models.CharField(max_length=30, unique=True)
    list_type           = models.CharField(max_length=10, null=False, choices=VALUESET_LIST_TYPE_CHOICES)   # LOV, LONG LOV, PopList
    # Format Validation Option
    fmt_type            = models.CharField(max_length=10, null=False, choices=VALUESET_FMT_VALIDATION_TYPE_CHOICES)
    fmt_max_size        = models.IntegerField(null=True)
    fmt_precision       = models.IntegerField(null=True)
    fmt_num             = models.BooleanField()
    fmt_uc              = models.BooleanField()    # uppercase
    fmt_rj              = models.BooleanField()    # Rith-justify and zero-fill numbers(0001)
    fmt_min_value       = models.IntegerField(null=True)
    fmt_max_value       = models.IntegerField(null=True)
    # Validation Option
    v_type              = models.CharField(max_length=10, choices=VALUESET_VALIDATION_TYPE_CHOICES)
    v_lookup            = models.ForeignKey(LookUpNode, null=True)
    v_rawsql            = models.TextField()

    # ========================================================
    created_by         = models.IntegerField(null=False)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

#
# Flexible Field
#
class KeyFlexField(models.Model):
    name               = models.CharField(max_length=30)
    

    # ========================================================
    created_by         = models.IntegerField(null=False)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

#
# 
#
class KeyFlexFieldSegment(models.Model):
    name               = models.CharField(max_length=30)
    column             = models.CharField(max_length=32)
    description        = models.CharField(max_length=255)
    # Display
    prompt             = models.CharField(max_length=255)
    desc_size          = models.IntegerField()
    disp_size          = models.IntegerField()
    value_set          = models.ForeignKey(ValueSet)
    # Qualifiers
    
    # ========================================================
    created_by         = models.IntegerField(null=False)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

#
#
#
class ProfileOption(models.Model):
    name               = models.CharField(max_length=100, unique=True)
    #application
    #user_profile_name
    #description
    start_date_active  = models.DateField(default=date.today)
    end_date_active    = models.DateField(null=True)
    sql_validation     = models.CharField(max_length=255)   # sql = "asdfasdf" column = ("", "")
    #hierarchy_type 
    #al_site_visible
    #al_app_visible
    #al_resp_visible
    #al_server_visible
    #al_org_visible
    #al_user_visible
    #al_site_updatable
    #al_app_updatable
    #al_resp_updatable
    #al_server_updatable
    #al_org_updatable
    #al_user_updatable
    # ========================================================
    created_by         = models.IntegerField(null=False)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

#
#
#
PROFILEOPTION_LEVEL_CHOICES = (
    ('SITE'   , 'site'),
    ('APP'    , 'app'),
    ('RESP'   , 'resp'),
    ('SERVER' , 'server'),
    ('ORG'    , 'org'),
    ('USER'   , 'user'),
)
class ProfileOptionValues(models.Model):
    option             = models.ForeignKey(ProfileOption)
    level_id           = models.CharField(max_length=10, null=False, choices=PROFILEOPTION_LEVEL_CHOICES)
    level_value        = models.IntegerField(null=False)    # 
    option_value       = models.CharField(max_length=255)  
    # ========================================================
    created_by         = models.IntegerField(null=False)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

    class Meta:
        unique_together = (
                ("option", "level_id", "level_value"),
                )

#
# 
#
class Function(models.Model):
    name               = models.CharField(max_length=100, unique=True)
    description        = models.CharField(max_length=240)
    app                = models.CharField(max_length=255, null=False)
    package            = models.CharField(max_length=255, null=False)
    paramters          = models.CharField(max_length=255, null=True)
    # ========================================================
    created_by         = models.IntegerField(null=False, default=fnd_global.get_user_id)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False, default=fnd_global.get_user_id)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

    def get_version(self):
        try:
            mod = __import__(self.package, {}, {}, [''])
        except:
            return 'Invalid package %s.' % self.package
        if hasattr(mod, '__version__'):
            return mod.__version__;
        else:
            return 'unknown'
    version = property(get_version)

    def get_svn_revision(self):
        try:
            mod = __import__(self.package, {}, {}, [''])
        except:
            return 'Invalid package %s.' % self.package
        if hasattr(mod, '__svn__'):
            return mod.__svn__;
        else:
            return (None, None, None)
    svn_revision = property(get_svn_revision)
    
    def get_urlconf(self):
        """
        TODO 出于性能原因,考虑将 [function.package + '.urls'] 直接作为参数,传入
        """
        func_mod = __import__(self.package, {}, {}, ['urls'])
        return func_mod.urls.__name__
    urlconf = property(get_urlconf)


#
# 用户映射,基于用户的访问控制Function和公共访问控制Function
# 这是一个
#
class FuncMapping(models.Model):
    regex_pattern      = models.CharField(max_length=100)
    type               = models.CharField(max_length=4)   # user, pub
    seq                = models.IntegerField(null=False)
    function           = models.ForeignKey(Function)
    # ========================================================
    created_by         = models.IntegerField(null=False)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================
    class Meta:
        unique_together = (
                ('regex_pattern', 'type'),
                ('type', 'seq'),
                )
#
# 
#
class Menu(models.Model):
    name               = models.CharField(max_length=100, unique=True)
    #type 
    description        = models.CharField(max_length=255)
    # ========================================================
    created_by         = models.IntegerField(null=False, default=fnd_global.get_user_id)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False, default=fnd_global.get_user_id)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

#
# 
#
class MenuItem(models.Model):
    p_menu             = models.ForeignKey(Menu, related_name="p_menu")
    seq                = models.IntegerField(null=False)
    prompt             = models.CharField(max_length=100, null=False)
    submenu            = models.ForeignKey(Menu, null=True, related_name="submenu")
    function           = models.ForeignKey(Function, null=True, related_name="function")
    description        = models.CharField(max_length=255)  
    # ========================================================
    created_by         = models.IntegerField(null=False, default=fnd_global.get_user_id)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False, default=fnd_global.get_user_id)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================
    class Meta:
        unique_together = (
                ("p_menu", "seq"),
                ("p_menu", "submenu"),
                ("p_menu", "function"),
                )
#
# 
#
class Responsibility(models.Model):
    name               = models.CharField(max_length=100, unique=True)
    menu               = models.ForeignKey(Menu)
    start_date_active  = models.DateField(default=date.today)
    end_date_active    = models.DateField(null=True)
    # ========================================================
    created_by         = models.IntegerField(null=False, default=fnd_global.get_user_id)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False, default=fnd_global.get_user_id)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================
#
#
#
class User(dj_auth_models.User):
    description    = models.CharField(max_length=240, blank=False)
    fax            = models.CharField(max_length=80, null=True)
    pwd_expiration_type    = models.IntegerField(default=0)   # 0:none 1:days 2:accesses
    pwd_lifespan     = models.IntegerField(default=0)
    pwd_begin_date   = models.DateField(default=date.today)
    pwd_accesses     = models.IntegerField(default=0)
    employee_id      = models.IntegerField(null=True)
    customer_id      = models.IntegerField(null=True)
    supplier_id      = models.IntegerField(null=True)
    person_party_id  = models.IntegerField(null=True)
    start_date_active  = models.DateField(default=date.today)
    end_date_active    = models.DateField(null=True)
    last_login         = models.DateTimeField(default=datetime.now)
    # ========================================================
    created_by         = models.IntegerField(null=False, default=fnd_global.get_user_id)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False, default=fnd_global.get_user_id)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================
    responsibilities   = models.ManyToManyField(Responsibility)


#=============================================== concurrent
class ConcurrentRequest(models.Model):
    request_id         = models.AutoField(primary_key=True)
    phase_code         = models.CharField(max_length=1)
    status_code        = models.CharField(max_length=1)
    os_process_id      = models.IntegerField(default=-1)
    has_sub_request    = models.BooleanField(default=False)
    is_sub_request     = models.BooleanField(default=False)
    responsibility_id  = models.IntegerField(default=fnd_global.get_resp_id)   # ref to Responsibility id 运行是的职责id
    program_id         = models.IntegerField()   # ref to ConcurrentProgram id
    output_file_mime   = models.CharField(max_length=100)   # ConcurrentProgram输出文件类型 output_file_type
    executable_id      = models.IntegerField()   # ref to ConcurrentExecutable id
    executable_method  = models.CharField(max_length=100)
    executable_file    = models.CharField(max_length=255)
    arguments_pickled  = models.TextField()      # program参数
    stdin_file         = models.CharField(max_length=255)  # 标准IO文件
    stdout_file        = models.CharField(max_length=255)  # 标准IO文件
    stderr_file        = models.CharField(max_length=255)  # 标准IO文件
    
    actual_start_date      = models.DateTimeField(null=True)   # 实际开始时间
    actual_completion_date = models.DateTimeField(null=True)   # 实际结束时间
    
    # ========================================================
    created_by         = models.IntegerField(default=fnd_global.get_user_id)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(default=fnd_global.get_user_id)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

class ConcurrentExecutable(models.Model):
    executable_id      = models.AutoField(primary_key=True)
    name               = models.CharField(max_length=255)
    method             = models.CharField(max_length=100)  # python_script, django_script 
    file               = models.CharField(max_length=255)  # 执行文件名,django_script时,执行的模块名
    icon_name          = models.CharField(max_length=30)
    execution_path     = models.CharField(max_length=255)
    
    # ========================================================
    created_by         = models.IntegerField(default=fnd_global.get_user_id)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(default=fnd_global.get_user_id)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

class ConcurrentProgram(models.Model):
    program_id         = models.AutoField(primary_key=True)
    name               = models.CharField(max_length=255)
    executable         = models.ForeignKey(ConcurrentExecutable, related_name="executable")
    # parameter_template = models.TextField() # 是个pickled字段,用于保存参数定义
    output_file_mime   = models.CharField(max_length=100)   # 输出文件类型 output_file_type
    # ========================================================
    created_by         = models.IntegerField(default=fnd_global.get_user_id)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(default=fnd_global.get_user_id)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================

#===============================================


# http://code.djangoproject.com/wiki/CookBookCategoryDataModel
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')

    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(p.category_name)
            more = self._recurse_for_parents(p)
            p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        return ' :: '

    def _parents_repr(self):
        p_list = self._recurse_for_parents(self)
        return self.get_separator().join(p_list)
    _parents_repr.short_description = "Category parents"

    # TODO: Does anybody know a better solution???
    def _pre_save(self):
        p_list = self._recurse_for_parents(self)
        if self.category_name in p_list:
            raise "You must not save a category in itself!"

    def __repr__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.category_name)
        return self.get_separator().join(p_list)

#~ class Category(models.Model):
    #~ name = models.CharField(core=True, max_length=200)
    #~ slug = models.SlugField(prepopulate_from=('name',))
    #~ parent = models.ForeignKey('self', blank=True, null=True, related_name='child')
    #~ description = models.TextField(blank=True,help_text="Optional")

    #~ class Admin:
        #~ list_display = ('name', '_parents_repr')

    #~ def __str__(self):
        #~ p_list = self._recurse_for_parents(self)
        #~ p_list.append(self.name)
        #~ return self.get_separator().join(p_list)

    #~ def get_absolute_url(self):
        #~ if self.parent_id:
            #~ return "/tag/%s/%s/" % (self.parent.slug, self.slug)
        #~ else:
            #~ return "/tag/%s/" % (self.slug)

    #~ def _recurse_for_parents(self, cat_obj):
        #~ p_list = []
        #~ if cat_obj.parent_id:
            #~ p = cat_obj.parent
            #~ p_list.append(p.name)
            #~ more = self._recurse_for_parents(p)
            #~ p_list.extend(more)
        #~ if cat_obj == self and p_list:
            #~ p_list.reverse()
        #~ return p_list
      
    #~ def get_separator(self):
        #~ return ' :: '

    #~ def _parents_repr(self):
        #~ p_list = self._recurse_for_parents(self)
        #~ return self.get_separator().join(p_list)
    #~ _parents_repr.short_description = "Tag parents"

    #~ def save(self):
      #~ p_list = self._recurse_for_parents(self)
      #~ if self.name in p_list:
          #~ raise validators.ValidationError("You must not save a category in itself!")
      #~ super(Category, self).save()

class Currency(models.Model):
    code      = models.CharField(max_length=15)  # Currency code
    language           = models.CharField(max_length=10)               # language code
    symbol             = models.CharField(max_length=12)               # The symbol denoting the currency
    name               = models.CharField(max_length=100)
    description        = models.CharField(max_length=255)              # Description
    enabled_flag       = models.BooleanField(default=True)             # Enabled Flag "Y","N","X" (X=never enabled)
    start_date_active  = models.DateField(default=date.today)
    end_date_active    = models.DateField(null=True)
    iso_flag           = models.BooleanField(default=True)             # Flag to indicate whether or not the currency is defined in ISO-4217
    # ========================================================
    created_by         = models.IntegerField(null=False)
    creation_date      = models.DateTimeField(auto_now_add=True)
    last_updated_by    = models.IntegerField(null=False)
    last_updated_date  = models.DateTimeField(auto_now=True)
    # ========================================================



# =========-site mailer-========================
class MailBoxManager(models.Manager):

    def inbox_for(self, user):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
        )

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )

    def trash_for(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
        )


class MailBox(models.Model):
    """
    A private message from user to user
    """
    subject = models.CharField(max_length=120)
    body = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_messages')
    recipient = models.ForeignKey(User, related_name='received_messages', null=True, blank=True)
    parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = MailBoxManager()
    
    def new(self):
        """returns whether the recipient has read the message or not"""
        if self.read_at is not None:
            return False
        return True
        
    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        if self.replied_at is not None:
            return True
        return False
    
    def __unicode__(self):
        return self.subject
    
    def get_absolute_url(self):
        return ('messages_detail', [self.id])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.sent_at = datetime.now()
        super(MailBox, self).save(force_insert, force_update) 
    
    class Meta:
        ordering = ['-sent_at']
#        verbose_name = _("Message")
#        verbose_name_plural = _("Messages")


# fallback for email notification if django-notification could not be found
#if "notification" not in settings.INSTALLED_APPS:
#    from messages.utils import new_message_email
#    signals.post_save.connect(new_message_email, sender=Message)

#==============================================notification start
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

QUEUE_ALL = getattr(settings, "NOTIFICATION_QUEUE_ALL", False)

# if this gets updated, the create() method below needs to be as well...
NOTICE_MEDIA = (
    ("1", _("Email")),
)

# how spam-sensitive is the medium
NOTICE_MEDIA_DEFAULTS = {
#    "1": 2 # email
    "1": 1 # email
}

class NoticeType(models.Model):

    label = models.CharField(_('label'), max_length=40)
    display = models.CharField(_('display'), max_length=50)
    description = models.CharField(_('description'), max_length=100)

    # by default only on for media with sensitivity less than or equal to this number
    default = models.IntegerField(_('default'))

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name = _("notice type")
        verbose_name_plural = _("notice types")

class NoticeSetting(models.Model):
    """
    Indicates, for a given user, whether to send notifications
    of a given type to a given medium.
    """

    user = models.ForeignKey(User, verbose_name=_('user'))
    notice_type = models.ForeignKey(NoticeType, verbose_name=_('notice type'))
    medium = models.CharField(_('medium'), max_length=1, choices=NOTICE_MEDIA)
    send = models.BooleanField(_('send'))

    class Meta:
        verbose_name = _("notice setting")
        verbose_name_plural = _("notice settings")
        unique_together = ("user", "notice_type", "medium")

class NoticeManager(models.Manager):

    def notices_for(self, user, archived=False, unseen=None, on_site=None):
        """
        returns Notice objects for the given user.

        If archived=False, it only include notices not archived.
        If archived=True, it returns all notices for that user.

        If unseen=None, it includes all notices.
        If unseen=True, return only unseen notices.
        If unseen=False, return only seen notices.
        """
        if archived:
            qs = self.filter(user=user)
        else:
            qs = self.filter(user=user, archived=archived)
        if unseen is not None:
            qs = qs.filter(unseen=unseen)
        if on_site is not None:
            qs = qs.filter(on_site=on_site)
        return qs

    def unseen_count_for(self, user, **kwargs):
        """
        returns the number of unseen notices for the given user but does not
        mark them seen
        """
        return self.notices_for(user, unseen=True, **kwargs).count()

class Notice(models.Model):

    user = models.ForeignKey(User, verbose_name=_('user'))
    message = models.TextField(_('message'))
    notice_type = models.ForeignKey(NoticeType, verbose_name=_('notice type'))
    added = models.DateTimeField(_('added'), default=datetime.now)
    unseen = models.BooleanField(_('unseen'), default=True)
    archived = models.BooleanField(_('archived'), default=False)
    on_site = models.BooleanField(_('on site'))

    objects = NoticeManager()

    def __unicode__(self):
        return self.message

    def archive(self):
        self.archived = True
        self.save()

    def is_unseen(self):
        """
        returns value of self.unseen but also changes it to false.

        Use this in a template to mark an unseen notice differently the first
        time it is shown.
        """
        unseen = self.unseen
        if unseen:
            self.unseen = False
            self.save()
        return unseen

    class Meta:
        ordering = ["-added"]
        verbose_name = _("notice")
        verbose_name_plural = _("notices")

    def get_absolute_url(self):
        return ("notification_notice", [str(self.pk)])
    get_absolute_url = models.permalink(get_absolute_url)

class NoticeQueueBatch(models.Model):
    """
    A queued notice.
    Denormalized data for a notice.
    """
    pickled_data = models.TextField()

class ObservedItemManager(models.Manager):

    def all_for(self, observed, signal):
        """
        Returns all ObservedItems for an observed object,
        to be sent when a signal is emited.
        """
        content_type = ContentType.objects.get_for_model(observed)
        observed_items = self.filter(content_type=content_type, object_id=observed.id, signal=signal)
        return observed_items

    def get_for(self, observed, observer, signal):
        content_type = ContentType.objects.get_for_model(observed)
        observed_item = self.get(content_type=content_type, object_id=observed.id, user=observer, signal=signal)
        return observed_item

class ObservedItem(models.Model):

    user = models.ForeignKey(User, verbose_name=_('user'))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    observed_object = generic.GenericForeignKey('content_type', 'object_id')

    notice_type = models.ForeignKey(NoticeType, verbose_name=_('notice type'))

    added = models.DateTimeField(_('added'), default=datetime.now)

    # the signal that will be listened to send the notice
    signal = models.TextField(verbose_name=_('signal'))

    objects = ObservedItemManager()

    class Meta:
        ordering = ['-added']
        verbose_name = _('observed item')
        verbose_name_plural = _('observed items')

    def send_notice(self):
        send([self.user], self.notice_type.label,
             {'observed': self.observed_object})
#==============================================notification end

