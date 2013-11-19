import logging

from Products.CMFPlone.utils import getToolByName
from zope.globalrequest import getRequest

from collective.whathappened.storage_manager import StorageManager
from collective.whathappened.subscription import Subscription
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
    subject = _(u"Account validation")
    if event.status['review_state'] == 'enabled':
        validated = True
    else:
        validated = False
    portal_url = getToolByName(context, 'portal_url')
    host = getToolByName(context, 'MailHost')
    mail_template = context.email_user_has_been_validated
    mail_text = mail_template(
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
