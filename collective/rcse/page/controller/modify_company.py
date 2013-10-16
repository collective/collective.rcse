from AccessControl import Unauthorized
from AccessControl.SecurityManagement import getSecurityManager
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
from collective.rcse.content.utils import createCompany
from collective.rcse.i18n import _


class ModifyCompanyFormSchema(interface.Interface):
    company = schema.Choice(
        title=_(u"Select your company"),
        vocabulary='collective.rcse.vocabulary.companies',
        required=False
        )
    new_company = schema.TextLine(
        title=_(u"Or create it"),
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
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, self.context):
            raise Unauthorized
        data, errors = self.extractData()
        if data['company'] is None and data['new_company'] is None:
            raise interfaces.WidgetActionExecutionError(
                'new_company',
                interface.Invalid(
                    _(u"You need to specify your company name.")
                    )
                )
        if errors:
            self.status = _(u"There were errors.")
            return
        if data['new_company'] is not None:
            self.context.company = data['new_company']
            self.context.company_id = createCompany(self.context,
                                                    self.request,
                                                    self.context.username,
                                                    self.context.company)
        else:
            self.context.company_id = data['company']
            companies = vocabularies.companies(self.context)
            self.context.company = companies.getTerm(data['company']).title
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u"Cancel"), name="cancel")
    def handleCancel(self, action):
        self.request.response.redirect(self.context.absolute_url())

class ModifyCompanyFormWrapper(FormWrapper):
    form = ModifyCompanyForm

    def update(self):
        super(ModifyCompanyFormWrapper, self).update()
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, self.context):
            raise Unauthorized
