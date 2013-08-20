from AccessControl import Unauthorized
from AccessControl.SecurityManagement import newSecurityManager,\
    getSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from plone.autoform.form import AutoExtensibleForm
from plone.dexterity.utils import createContentInContainer
from plone.z3cform.layout import FormWrapper
from Products.CMFCore.permissions import ModifyPortalContent
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


class ModifyCompanyFormSchema(interface.Interface):
    company = schema.Choice(
        title=_(u"Company"),
        vocabulary='collective.rcse.vocabulary.companies'
        )
    new_company = schema.TextLine(
        title=_(u"New company"),
        required=False
        )


class ModifyCompanyFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(ModifyCompanyFormSchema)

    def __init__(self, context):
        self.context = context


class ModifyCompanyForm(AutoExtensibleForm, form.Form):
    schema = ModifyCompanyFormSchema
    enableCSRFProtection = True
    label = _(u"Modify your company")

    @button.buttonAndHandler(_(u"Submit"), name="submit")
    def handleApply(self, action):
        data, errors = self.extractData()
        if data['company'] == '__new_company' or data['company'] == '':
            if not data['new_company']:
                raise interfaces.WidgetActionExecutionError(
                    'new_company',
                    interface.Invalid(
                        _(u"You need to specify your company name.")
                        )
                    )
        if errors:
            self.status = _(u"There were errors.")
            return
        if data['company'] == '__new_company' or data['company'] == '':
            data['company'] = data['new_company']
            data['company_id'] = self._createNewCompany(data)
        else:
            data['company_id'] = data['company']
            companies = vocabularies.companies(self.context)
            data['company'] = companies.getTerm(data['company']).title
        self.context.company = data['company']
        self.context.company_id = data['company_id']
        self.request.response.redirect(self.context.absolute_url())

    def _createNewCompany(self, data):
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name=u'plone_portal_state')
        directory = portal_state.portal()['companies_directory']
        self.mtool = getToolByName(self.context, 'portal_membership')
        self._security_manager = getSecurityManager()
        self._sudo('Manager')
        company = createContentInContainer(
            directory,
            'collective.rcse.company',
            title=data['company']
            )
        company.changeOwnership(self.mtool.getMemberById(self.context.username))
        company.manage_setLocalRoles(self.context.username, ['Owner'])
        company.setCreators([self.context.username])
        company.reindexObjectSecurity()
        self._sudo()
        return company.id

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


class ModifyCompanyFormWrapper(FormWrapper):
    form = ModifyCompanyForm

    def update(self):
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, self.context):
            raise Unauthorized
