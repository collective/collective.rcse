# -*- coding: utf-8 -*-
from email.header import Header
import logging

from Products.CMFPlone.utils import getToolByName
from zope.globalrequest import getRequest
from zope.event import notify
from zope.i18n import translate

from collective.whathappened.storage_manager import StorageManager
from collective.whathappened.subscription import Subscription
from collective.rcse import cache
from collective.rcse.event import UserRolesModifiedOnObjectEvent
from collective.rcse.i18n import _

logger = logging.getLogger(__name__)


def handle_content_creation(context, event):
    context_path = '/'.join(context.getPhysicalPath())
    if context.getPhysicalPath()[1] != 'home' and \
            context.getPhysicalPath()[2] != 'home':
        return
    user = context.Creator()
    if not user:
        logger.warning('context %s has no creator.' % context)
        return
    storage = StorageManager(context)
    storage.initialize()
    storage.setUser(user)
    storage.saveSubscription(Subscription(context_path, True))
    storage.terminate()
    notify(UserRolesModifiedOnObjectEvent(user, context))


def handle_group_modification(context, event):
    cache.clearCacheKeyGroupTitle(context)


def handle_user_validation(context, event):
    mtool = getToolByName(context, 'membrane_tool')
    mtool.reindexObject(context)
    if event.old_state.id != 'pending':
        return
    if event.status['action'] not in ('approve', 'decline'):
        return
    _sendMail(context, event)


def _sendMail(context, event):
    email = context.email
    subject = translate(_(u"Account validation"), context=getRequest())
    if event.status['review_state'] == 'enabled':
        validated = True
    else:
        validated = False
    portal_url = getToolByName(context, 'portal_url')
    host = getToolByName(context, 'MailHost')
    from_email = host.email_from_address
    subject = Header(subject, 'utf-8').encode()
    mail_template = context.email_user_has_been_validated
    mail_text = mail_template(
        from_email=from_email,
        subject=subject,
        email=email,
        portal_url=portal_url(),
        validated=validated,
        request=getRequest()
    )
    try:
        host.send(mail_text.encode('utf8'))
    except:
        # @TODO
        pass
