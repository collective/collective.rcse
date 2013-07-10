from AccessControl import Unauthorized
from AccessControl.SecurityManagement import newSecurityManager,\
    getSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from plone.autoform.form import AutoExtensibleForm
from plone.dexterity import utils
from plone.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from z3c.form import form
from z3c.form import button
from zope import component
from zope import interface

from collective.rcse.content.member import IMember
from collective.rcse.i18n import _

class RegisterFormSchema(IMember):
    pass


class RegisterFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(RegisterFormSchema)

    def __init__(self, context):
        self.context = context


class RegisterForm(AutoExtensibleForm, form.Form):
    schema = RegisterFormSchema
    enableCSRFProtection = True
    label = _(u"Register your information")

    def update(self):
        super(RegisterForm, self).update()

    @button.buttonAndHandler(_(u"Submit"), name="submit")
    def handleApply(self, action):
        self.mtool = getToolByName(self.context, 'portal_membership')
        user = self.mtool.getAuthenticatedMember()
        if type(user.getProperty('username')) != object:
            raise Unauthorized(_(u"You are already registered."))
        data, errors = self.extractData()
        if errors:
            self.status = _(u"There were errors.")
            return
        self._createUser(user.getUserId(), data)
        self.request.response.redirect('@@register')

    def _createUser(self, username, data):
        # @TODO check there is no content with the same username
        container = self.context.unrestrictedTraverse('users_directory')
        if username in container:
            raise Unauthorized(_(u"You are already registered."))
        self._security_manager = getSecurityManager()
        self.wtool = getToolByName(self.context, 'portal_workflow')
        self._sudo('Manager')
        data['username'] = username
        user = utils.createContent('collective.rcse.member', **data)
        utils.addContentToContainer(container, user)
        item = user.__of__(container)
        self.wtool.doActionFor(item, 'approve')
        self._sudo(None)

    def _sudo(self, role):
        """Give admin power to the current call"""
        if role is not None:
            if self.mtool.getAuthenticatedMember().has_role(role):
                return
            sm = getSecurityManager()
            acl_users = getToolByName(self.context, 'acl_users')
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', [role], ''
            )
            tmp_user = tmp_user.__of__(acl_users)
            newSecurityManager(None, tmp_user)
        else:
            setSecurityManager(self._security_manager)


class RegisterFormWrapper(FormWrapper):
    form = RegisterForm

    def update(self):
        super(RegisterFormWrapper, self).update()
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.isAnonymousUser():
            raise Unauthorized(_(u"You must be connected to do this."))
        user = mtool.getAuthenticatedMember()
        if type(user.getProperty('username')) != object:
            raise Unauthorized(_(u"You are already registered."))
