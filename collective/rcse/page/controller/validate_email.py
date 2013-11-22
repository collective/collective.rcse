import os
from smtplib import SMTPException
from AccessControl import Unauthorized
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser import BrowserView

from collective.rcse.i18n import _
from collective.rcse.page.controller.person_view import \
    AuthenticatedMemberInfoView


class ValidateEmailView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.message = _(u'Your email has been validated.')

    def __call__(self):
        memberview = AuthenticatedMemberInfoView(self.context, self.request)
        try:
            memberview.update()
        except ValueError:
            raise Unauthorized
        self.memberinfo = memberview.get_membrane()
        key = self.request.get('key', None)
        if key is None:
            self.message = _(u'No key provided.')
        elif key != self.memberinfo.email_validation:
            self.message = _(u'Bad key.')
        else:
            self.memberinfo.email_validation = 'ok'
        return self.index()


class SendValidationEmailView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.error = False
        self.message = _(u'Email has been sent.')

    def __call__(self):
        memberview = AuthenticatedMemberInfoView(self.context, self.request)
        try:
            memberview.update()
        except ValueError:
            raise Unauthorized
        self.memberinfo = memberview.get_membrane()
        if self.memberinfo.email_validation == 'ok':
            self.message = _(u'Your email has already been validated.')
            return self.index()
        self.generateNewKey()
        try:
            self.sendValidationEmail()
        except SMTPException:
            self.error = True
        return self.index()

    def generateNewKey(self):
        if self.memberinfo.email_validation == 'ok':
            return None
        key = os.urandom(16).encode('hex')
        self.memberinfo.email_validation = key
        return key

    def sendValidationEmail(self):
        host = getToolByName(self.context, 'MailHost')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        subject = portal.Title
        validation_url = '%s/@@validate_email?key=%s' % (
            portal.absolute_url(),
            self.memberinfo.email_validation
        )
        mail_template = portal.email_validate_email
        mail_text = mail_template(
            subject=subject,
            email=self.memberinfo.email,
            validation_url=validation_url,
            request=self.request
        )
        host.send(mail_text.encode('utf8'))


def generateKeyAndSendEmail(context, request, memberinfo):
    key = os.urandom(16).encode('hex')
    memberinfo.email_validation = key
    host = getToolByName(context, 'MailHost')
    portal = getToolByName(context, 'portal_url').getPortalObject()
    subject = portal.Title
    validation_url = '%s/@@validate_email?key=%s' % (
        portal.absolute_url(),
        memberinfo.email_validation
    )
    mail_template = portal.email_validate_email
    mail_text = mail_template(
        subject=subject,
        email=memberinfo.email,
        validation_url=validation_url,
        request=request
    )
    host.send(mail_text.encode('utf8'))
