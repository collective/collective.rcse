from AccessControl import Unauthorized
from plone.autoform.form import AutoExtensibleForm
from plone.z3cform.layout import FormWrapper
from z3c.form import form
from z3c.form import button
from zope import component
from zope import interface

from collective.rcse.settings import IPersonalPreferences
from collective.rcse.i18n import _


class PersonalPreferencesFormSchema(IPersonalPreferences):
    pass


class PersonalPreferencesFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(PersonalPreferencesFormSchema)

    def __init__(self, context):
        self.context = context


class PersonalPreferencesForm(AutoExtensibleForm, form.Form):
    schema = PersonalPreferencesFormSchema
    enableCSRFProtection = True
    label = _("Personal preferences")

    def update(self):
        super(PersonalPreferencesForm, self).update()
        self.member = self.context.restrictedTraverse('auth_memberinfo')
        self.member.update()
        self.member_context = self.member.get_membrane()
        if self.member_context is None:
            raise Unauthorized
        self.settings = self.member_context.restrictedTraverse('get_settings')
        self._updateSettings()

    def _updateSettings(self):
        for field in self.fields:
            if field in IPersonalPreferences.names():
                try:
                    value = self.settings.get(field)
                    self.fields[field].field.default = value
                except KeyError:
                    pass

    @button.buttonAndHandler(_(u"Save"), name="save")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            return
        self.member = self.context.restrictedTraverse('auth_memberinfo')
        self.member.update()
        self.member_context = self.member.get_membrane()
        self.settings = self.member_context.restrictedTraverse('get_settings')
        for key, value in data.items():
            if key in IPersonalPreferences.names():
                self.settings.set(key, value)


class PersonalPreferencesFormWrapper(FormWrapper):
    form = PersonalPreferencesForm
