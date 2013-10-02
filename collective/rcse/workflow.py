from Products.CMFPlone.utils import getToolByName
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest

from collective.rcse.i18n import _
from collective.rcse.content.utils import createCompany


def handle_user_validation(context, event):
    if event.old_state.id != 'pending':
        return
    if event.status['action'] not in ('approve', 'decline'):
        return
    _sendMail(context, event)
    _createCompanyIfNotExists(context, event)


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


def _createCompanyIfNotExists(context, event):
    if event.new_state.id != 'enabled':
        return
    request = getRequest()
    portal_state = getMultiAdapter((context, request),
                                   name=u'plone_portal_state')
    directory = portal_state.portal()['companies_directory']
    if not context.company_id or context.company_id not in directory:
        mtool = getToolByName(context, 'portal_membership')
        context.company_id = createCompany(context, request)
