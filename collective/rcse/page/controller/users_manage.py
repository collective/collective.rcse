
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


class ManageUsersFormSchema(interface.Interface):
    """Form used by user to register."""
    user_id = schema.ASCIILine(title=_(u"Users uuid"))


class ManageUsersFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(ManageUsersFormSchema)

    def __init__(self, context):
        self.context = context
        self.user_id = None


class ManageUsersForm(AutoExtensibleForm, form.Form):
    schema = ManageUsersFormSchema
    enableCSRFProtection = True

    def updateActions(self):
        super(ManageUsersForm, self).updateActions()
        self.actions['approve'].addClass('btn-primary')

    @button.buttonAndHandler(_(u"Approve"), name="approve")
    def handleApprove(self, action):
        self._handleUser('approve')

    @button.buttonAndHandler(_(u"Decline"), name="decline")
    def handleDisapprove(self, action):
        self._handleUser('decline')

    def _handleUser(self, action):
        data, errors = self.extractData()
        if errors:
            return
        user = self._getUserItem(data['user_id'])
        if user is None:
            return
        wtool = getToolByName(self.context, 'portal_workflow')
        try:
            wtool.doActionFor(user, action)
        except WorkflowException:
            return
        self.request.response.redirect('@@rcse_users_manage')

    def _getUserItem(self, id):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        try:
            user = portal['users_directory'][id]
        except KeyError:
            user = None
        return user


class ManageUsersView(UsersDirectoryView):
    def getUsersForms(self):
        users = [user for user in self.getMembers(batch=False)
                 if user.review_state == 'pending']
        forms = []
        for user in users:
            form = {}
            form['user'] = user
            form['form'] = ManageUsersForm(self.context, self.request)
            form['form'].next_url = '/@@rcse_users_manage'
            form['form'].update()
            form['form'].widgets['user_id'].mode = HIDDEN_MODE
            form['form'].widgets['user_id'].value = user.id
            forms.append(form)
        return forms
