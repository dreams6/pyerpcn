# -*- coding: utf-8 -*- 

try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import render_to_string

from django.core.exceptions import ImproperlyConfigured

from django.contrib.sites.models import Site

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext, get_language, activate

from pyerp.fnd.models import *
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)

# favour django-mailer but fall back to django.core.mail
if 'mailer' in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

class LanguageStoreNotAvailable(Exception):
    pass




def get_notification_setting(user, notice_type, medium):
    try:
        return NoticeSetting.objects.get(user=user, notice_type=notice_type, medium=medium)
    except NoticeSetting.DoesNotExist:
        default = (NOTICE_MEDIA_DEFAULTS[medium] <= notice_type.default)
        setting = NoticeSetting(user=user, notice_type=notice_type, medium=medium, send=default)
        setting.save()
        return setting

def should_send(user, notice_type, medium):
    return get_notification_setting(user, notice_type, medium).send

def create_notice_type(label, display, description, default=2, verbosity=1):
    """
    Creates a new NoticeType.

    This is intended to be used by other apps as a post_syncdb manangement step.
    """
    try:
        notice_type = NoticeType.objects.get(label=label)
        updated = False
        if display != notice_type.display:
            notice_type.display = display
            updated = True
        if description != notice_type.description:
            notice_type.description = description
            updated = True
        if default != notice_type.default:
            notice_type.default = default
            updated = True
        if updated:
            notice_type.save()
            if verbosity > 1:
                print "Updated %s NoticeType" % label
    except NoticeType.DoesNotExist:
        NoticeType(label=label, display=display, description=description, default=default).save()
        if verbosity > 1:
            print "Created %s NoticeType" % label

def get_notification_language(user):
    """
    Returns site-specific notification language for this user. Raises
    LanguageStoreNotAvailable if this site does not use translated
    notifications.
    """
    if getattr(settings, 'NOTIFICATION_LANGUAGE_MODULE', False):
        try:
            app_label, model_name = settings.NOTIFICATION_LANGUAGE_MODULE.split('.')
            model = models.get_model(app_label, model_name)
            language_model = model._default_manager.get(user__id__exact=user.id)
            if hasattr(language_model, 'language'):
                return language_model.language
        except (ImportError, ImproperlyConfigured, model.DoesNotExist):
            raise LanguageStoreNotAvailable
    raise LanguageStoreNotAvailable

def get_formatted_messages(formats, label, context):
    """
    Returns a dictionary with the format identifier as the key. The values are
    are fully rendered templates with the given context.
    """
    format_templates = {}
    for format in formats:
        # conditionally turn off autoescaping for .txt extensions in format
        if format.endswith(".txt"):
            context.autoescape = False
        else:
            context.autoescape = True
        format_templates[format] = render_to_string((
            'user/mailbox/%s/%s' % (label, format),
            'user/mailbox/%s' % format), context_instance=context)
    return format_templates

def send_now(users, label, extra_context=None, on_site=True):
    """
    Creates a new notice.

    This is intended to be how other apps create new notices.

    notification.send(user, 'friends_invite_sent', {
        'spam': 'eggs',
        'foo': 'bar',
    )
    
    You can pass in on_site=False to prevent the notice emitted from being
    displayed on the site.
    """
    if extra_context is None:
        extra_context = {}
    
    notice_type = NoticeType.objects.get(label=label)

    current_site = Site.objects.get_current()
#    notices_url = u"http://%s%s" % (
#        unicode(current_site),
#        reverse("notification_notices"),
#    )
    notices_url = "========"

    current_language = get_language()

    formats = (
        'short.txt',
        'full.txt',
        'notice.html',
        'full.html',
    ) # TODO make formats configurable

    for user in users:
        recipients = []
        # get user language for user from language store defined in
        # NOTIFICATION_LANGUAGE_MODULE setting
        try:
            language = get_notification_language(user)
        except LanguageStoreNotAvailable:
            language = None

        if language is not None:
            # activate the user's language
            activate(language)

        # update context with user specific translations
        context = Context({
            "user": user,
            "notice": ugettext(notice_type.display),
            "notices_url": notices_url,
            "current_site": current_site,
        })
        context.update(extra_context)

        # get prerendered format messages
        messages = get_formatted_messages(formats, label, context)

        # Strip newlines from subject
        subject = ''.join(render_to_string('user/mailbox/email_subject.txt', {
            'message': messages['short.txt'],
        }, context).splitlines())

        body = render_to_string('user/mailbox/email_body.txt', {
            'message': messages['full.txt'],
        }, context)

        notice = Notice.objects.create(user=user, message=messages['notice.html'],
            notice_type=notice_type, on_site=on_site)
        if should_send(user, notice_type, "1") and user.email: # Email
            recipients.append(user.email)
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
        #print send_mail("dddd", "ades", settings.DEFAULT_FROM_EMAIL, recipients)

    # reset environment to original language
    activate(current_language)

def send(*args, **kwargs):
    """
    A basic interface around both queue and send_now. This honors a global
    flag NOTIFICATION_QUEUE_ALL that helps determine whether all calls should
    be queued or not. A per call ``queue`` or ``now`` keyword argument can be
    used to always override the default global behavior.
    """
    queue_flag = kwargs.pop("queue", False)
    now_flag = kwargs.pop("now", False)
    assert not (queue_flag and now_flag), "'queue' and 'now' cannot both be True."
    if queue_flag:
        return queue(*args, **kwargs)
    elif now_flag:
        return send_now(*args, **kwargs)
    else:
        if QUEUE_ALL:
            return queue(*args, **kwargs)
        else:
            return send_now(*args, **kwargs)
        
def queue(users, label, extra_context=None, on_site=True):
    """
    Queue the notification in NoticeQueueBatch. This allows for large amounts
    of user notifications to be deferred to a seperate process running outside
    the webserver.
    """
    if extra_context is None:
        extra_context = {}
    if isinstance(users, QuerySet):
        users = [row["pk"] for row in users.values("pk")]
    else:
        users = [user.pk for user in users]
    notices = []
    for user in users:
        notices.append((user, label, extra_context, on_site))
    NoticeQueueBatch(pickled_data=pickle.dumps(notices).encode("base64")).save()

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

def observe(observed, observer, notice_type_label, signal='post_save'):
    """
    Create a new ObservedItem.

    To be used by applications to register a user as an observer for some object.
    """
    notice_type = NoticeType.objects.get(label=notice_type_label)
    observed_item = ObservedItem(user=observer, observed_object=observed,
                                 notice_type=notice_type, signal=signal)
    observed_item.save()
    return observed_item

def stop_observing(observed, observer, signal='post_save'):
    """
    Remove an observed item.
    """
    observed_item = ObservedItem.objects.get_for(observed, observer, signal)
    observed_item.delete()

def send_observation_notices_for(observed, signal='post_save'):
    """
    Send a notice for each registered user about an observed object.
    """
    observed_items = ObservedItem.objects.all_for(observed, signal)
    for observed_item in observed_items:
        observed_item.send_notice()
    return observed_items

def is_observing(observed, observer, signal='post_save'):
    if isinstance(observer, AnonymousUser):
        return False
    try:
        observed_items = ObservedItem.objects.get_for(observed, observer, signal)
        return True
    except ObservedItem.DoesNotExist:
        return False
    except ObservedItem.MultipleObjectsReturned:
        return True

def handle_observations(sender, instance, *args, **kw):
    send_observation_notices_for(instance)
