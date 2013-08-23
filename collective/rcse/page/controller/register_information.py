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
from z3c.form import interfaces
from zope import component
from zope import interface
from zope import schema

from collective.rcse.content.member import IMember
from collective.rcse.content.member import vocabularies
from collective.rcse.i18n import _


class RegisterInformationFormSchema(IMember):
    company = schema.Choice(
        title=_(u"Company"),
        vocabulary='collective.rcse.vocabulary.companies'
        )
    new_company = schema.TextLine(
        title=_(u"New company"),
        required=False
        )


class RegisterInformationFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(RegisterInformationFormSchema)

    def __init__(self, context):
        self.context = context


class RegisterInformationForm(AutoExtensibleForm, form.Form):
    schema = RegisterInformationFormSchema
    enableCSRFProtection = True
    label = _(u"Register your information")

    @button.buttonAndHandler(_(u"Submit"), name="submit")
    def handleApply(self, action):
        self.mtool = getToolByName(self.context, 'portal_membership')
        user = self.mtool.getAuthenticatedMember()
        data, errors = self.extractData()
        self._checkForm(user, data)
        if errors:
            self.status = _(u"There were errors.")
            return
        if data['company'] == '__new_company' or data['company'] == '':
            data['company'] = data['new_company']
        else:
            data['company_id'] = data['company']
            companies = vocabularies.companies()
            data['company'] = companies.getTerm(data['company']).title
        self._createUser(user.getId(), data)
        portal_url = getToolByName(self.context, "portal_url")
        self.request.response.redirect(
            '%s/@@personal-information' % portal_url()
            )

    def _checkForm(self, user, data):
        if type(user.getProperty('username')) != object:
            raise interfaces.ActionExecutionError(
                interface.Invalid(_(u"You are already registered."))
                )
        if data['company'] == '__new_company' or data['company'] == '':
            if not data['new_company']:
                raise interfaces.WidgetActionExecutionError(
                    'new_company',
                    interface.Invalid(
                        _(u"You need to specify your company name.")
                        )
                    )

    def _createUser(self, username, data):
        container = self.context.unrestrictedTraverse('users_directory')
        mtool = getToolByName(self.context, 'membrane_tool')
        results = mtool.searchResults(getUserName=username)
        if len(results) > 0:
            raise Unauthorized, _(u"You are already registered.")
        data['username'] = username
        self._security_manager = getSecurityManager()
        self._sudo('Manager')
        item = utils.createContentInContainer(
            container,
            'collective.rcse.member',
            checkConstraints=False,
            **data)
        item.manage_setLocalRoles(username, ['Owner'])
        item.reindexObjectSecurity()
        self._sudo()

    def _sudo(self, role=None):
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


class RegisterInformationFormWrapper(FormWrapper):
    form = RegisterInformationForm

    def getMemberInfo(self):
        self.portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
            )
        self.member = self.portal_state.member()
        #get member data
        catalog = getToolByName(self.context, 'membrane_tool')
        self.username = self.member.getUserName()
        self.member_data = None
        if self.username:
            results = catalog(getUserName=self.username)
            if results:
                self.member_data = results[0].getObject()

    def update(self):
        super(RegisterInformationFormWrapper, self).update()
        self.getMemberInfo()
        portal_url = self.portal_state.portal_url()
        if self.portal_state.anonymous():
            self.request.response.redirect('%s/login' % portal_url)
        if self.member_data is not None:
            self.request.response.redirect(
                '%s/@@personal-information' % portal_url
                )
