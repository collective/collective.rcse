import logging

from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.Five.browser import BrowserView
from z3c.form import form
from z3c.form import button
from z3c.form import interfaces
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.browser.password import PasswordFieldWidget
from zope import component
from zope import interface
from zope import schema

from collective.rcse.i18n import _
from collective.rcse.page.controller.users_directory import UsersDirectoryView
from Products.statusmessages.interfaces import IStatusMessage

logger = logging.getLogger(__name__)


class ManageUserFormSchema(interface.Interface):
    """Form used by user to register."""
    user_id = schema.ASCIILine(title=_(u"Users uuid"))


class ManageUserFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(ManageUserFormSchema)

    def __init__(self, context):
        self.context = context
        self.user_id = None


class ManageUserForm(AutoExtensibleForm, form.Form):
    schema = ManageUserFormSchema
    enableCSRFProtection = True

    def updateActions(self):
        super(ManageUserForm, self).updateActions()
        self.actions['approve'].addClass('btn-primary')

    def _handleUser(self, action):
        data, errors = self.extractData()
        message = IStatusMessage(self.request)
        if errors:
            message.add("%s" % errors, type="error")
            logger.info(errors)
            return
        user = self._getUserItem(data['user_id'])
        if user is None:
            logger.info("user data not found")
            message.add(_(u"user not found in directory"), type="error")
            return
        wtool = getToolByName(self.context, 'portal_workflow')
        try:
            wtool.doActionFor(user, action)
        except WorkflowException as e:
            message.add(_(u"Can't enable the member ${user}",
                          mapping={'user': user}),
                        type="error")
            logger.error("Can't enable the member %s: %s" %
                         (user.username, e.message))
            return
        referer = self.request.get("HTTP_REFERER")
        if not referer:
            referer = self.context.absolute_url()
        self.request.response.redirect(referer)

    def _getUserItem(self, id):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        try:
            user = portal['users_directory'][id]
        except KeyError:
            user = None
        return user


class ManagePendingUserForm(ManageUserForm):

    @button.buttonAndHandler(_(u"Approve"), name="approve")
    def handleApprove(self, action):
        self._handleUser('approve')

    @button.buttonAndHandler(_(u"Decline"), name="decline")
    def handleDisapprove(self, action):
        self._handleUser('decline')


class ManageDisabledUserForm(ManageUserForm):

    @button.buttonAndHandler(_(u"Enable"), name="enable")
    def handleApprove(self, action):
        self._handleUser('enable')

    @button.buttonAndHandler(_(u"Delete"), name="delete")
    def handleApprove(self, action):
        data, errors = self.extractData()
        userid = data['user_id']
        self.context.manage_delObjects([userid])
        msg = _(u"User ${user} has been deleted",
                mapping={'user': userid})
        IStatusMessage(self.request).add(msg)
        referer = self.request.get("HTTP_REFERER")
        if not referer:
            referer = self.context.absolute_url()
        self.request.response.redirect(referer)

class ManagePendingUsersView(UsersDirectoryView):
    state = "pending"
    def getUsersForms(self):
        users = self.getMembers(review_state=self.state)
        forms = []
        for user in users:
            user['form'] = ManagePendingUserForm(self.context, self.request)
            user['form'].next_url = '/@@rcse_users_manage'
            user['form'].update()
            user['form'].widgets['user_id'].mode = HIDDEN_MODE
            user['form'].widgets['user_id'].value = user["dataid"]
            forms.append(user)
        return forms


class ManageDisabledUsersView(UsersDirectoryView):
    state = "disabled"
    def getUsersForms(self):
        users = self.getMembers(review_state=self.state)
        forms = []
        for user in users:
            user['form'] = ManageDisabledUserForm(self.context, self.request)
            user['form'].next_url = '/@@rcse_users_manage'
            user['form'].update()
            user['form'].widgets['user_id'].mode = HIDDEN_MODE
            user['form'].widgets['user_id'].value = user["dataid"]
            forms.append(user)
        return forms
