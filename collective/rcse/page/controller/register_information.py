import datetime
import re
import logging

from plone.autoform.form import AutoExtensibleForm
from plone.dexterity import utils
from plone.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from z3c.form import form
from z3c.form import button
from z3c.form import interfaces
from zope.container.interfaces import INameChooser
from zope import component
from zope import interface
from zope import schema

from collective.rcse.content.member import IMember
from collective.rcse.content.member import vocabularies
from collective.rcse.content.utils import createCompany
from collective.rcse.page.controller.validate_email import generateKeyAndSendEmail
from collective.rcse.i18n import _
from collective.rcse.utils import sudo, createNotification

logger = logging.getLogger("collective.rcse")


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


def _attrGender(value):
    v = {'MALE': 'male',
         'FEMALE': 'female'}
    return v[value]


def _attrCity(value):
    if value[0] == '{':
        p = re.compile('city:([^,}]+)')
        m = p.findall(value)
        if m:
            return m[0]
    return value


def _attrLang(value):
    v = {'fr': 'French',
         'en': 'English'}
    if value[0] not in ('[', '{'):
        if value in v.keys():
            return [v[value]]
        return [value]
    # Facebook
    p = re.compile('name:([^,}]+)')
    m = p.findall(value)
    return list(m)


class RegisterInformationForm(AutoExtensibleForm, form.Form):
    schema = RegisterInformationFormSchema
    enableCSRFProtection = True
    label = _(u"Register your information")

    # CAS Attribute to field name
    attributes_key = {
        'gender': 'gender',
        'email': 'email',
        'email-address': 'email',
        'first-name': 'first_name',
        'last-name': 'last_name',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'given_name': 'first_name',
        'family_name': 'last_name',
        'language': 'lang',
        'languages': 'lang',
        'locale': 'lang',
        'bio': 'bio',
        'introduction': 'bio',
        'location': 'city',
        }
    # field name : function taking value returning new value
    attributes_value = {
        'gender': _attrGender,
        'city': _attrCity,
        'lang': _attrLang,
        }

    def update(self):
        super(RegisterInformationForm, self).update()
        sdm = getToolByName(self.context, 'session_data_manager')
        session = sdm.getSessionData(create=False)
        attributes = session.get('cas_attributes', {})
        for attribute, value in attributes.items():
            if attribute in self.attributes_key.keys():
                key = self.attributes_key[attribute]
                if key in self.attributes_value.keys():
                    value = self.attributes_value[key](value)
                self._updateWidgets(key, value)
            else:
                logger.info("Unused attribute %s: %s" % (attribute, value))

    def _updateWidgets(self, key, value):
        if key in self.widgets.keys():
            self.widgets[key].value = value
            return
        for group in self.groups:
            if key in group.widgets.keys():
                group.widgets[key].value = value
                return
        raise KeyError(key)

    @button.buttonAndHandler(_(u"Submit"), name="submit")
    def handleApply(self, action):
        self.mtool = getToolByName(self.context, 'portal_membership')
        data, errors = self.extractData()
        self._checkForm(data)
        if errors:
            self.status = _(u"There were errors.")
            return
        self.member = self.mtool.getAuthenticatedMember()
        self._updateDataCompany(data, self.member.getId())
        self._updateUser(self.member.getId(), data)
        self._renameUserContent()
        self._sendMailToUser()
        self._sendNotificationToAdmin()
        portal_url = getToolByName(self.context, "portal_url")
        self.request.response.redirect(
            '%s/@@personal-information' % portal_url()
            )

    def _updateDataCompany(self, data, username):
        if data['company'] == '__new_company' or data['company'] == '':
            data['company'] = data['new_company']
            data['company_id'] = createCompany(self.context,
                                               self.request,
                                               username,
                                               data['company'])
        else:
            data['company_id'] = data['company']
            companies = vocabularies.companies(self.context)
            data['company'] = companies.getTerm(data['company']).title

    def _checkForm(self, data):
        if data['company'] == '__new_company' or data['company'] == '':
            if not data['new_company']:
                raise interfaces.WidgetActionExecutionError(
                    'new_company',
                    interface.Invalid(
                        _(u"You need to specify your company name.")
                        )
                    )

    def _updateUser(self, username, data, member_data=None):
        self.catalog = getToolByName(self, 'membrane_tool')
        if member_data is not None:
            self.member_data = member_data
        else:
            self.member_data = None
            if username:
                results = self.catalog(getUserName=username)
                if results:
                    self.member_data = results[0].getObject()
        if self.member_data is None:
            raise ValueError("No user found.")
        for key, value in data.items():
            setattr(self.member_data, key, value)

    def _sendMailToUser(self):
        generateKeyAndSendEmail(self.context, self.request,
                                self.member_data)

    def _sendNotificationToAdmin(self):
        where = '/'.join(self.member_data.getPhysicalPath())
        groups = getToolByName(self.context, 'portal_groups')
        group = groups.getGroupById('Site Administrators')
        if group is None:
            return
        for member in group.getGroupMembers():
            createNotification('waiting_for_validation',
                               where,
                               datetime.datetime.now(),
                               [self.member_data.username],
                               member.id)

    @sudo()
    def _renameUserContent(self):
        directory = self.member_data.aq_parent
        title = '%s %s' % (self.member_data.first_name,
                           self.member_data.last_name)
        self.member_data.setTitle(title)
        new_id = INameChooser(directory).chooseName(title, self.member_data)
        self.catalog.unindexObject(self.member_data)
        directory.manage_renameObject(self.member_data.id, new_id)
        self.catalog.indexObject(self.member_data)


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
        if self.member_data and self.member_data.company_id is not None:
            self.request.response.redirect(
                '%s/@@personal-information' % portal_url
                )
