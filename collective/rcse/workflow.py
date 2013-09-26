from Products.CMFPlone.utils import getToolByName
from zope.globalrequest import getRequest

from collective.rcse.i18n import _


def handle_user_validation(context, event):
    if event.old_state.id != 'pending':
        return
    if event.status['action'] not in ('approve', 'decline'):
        return
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
    host.send(mail_text.encode('utf8'))
