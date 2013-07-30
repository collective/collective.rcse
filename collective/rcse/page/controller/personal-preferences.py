from plone.autoform.form import AutoExtensibleForm
from plone.z3cform.layout import FormWrapper
from z3c.form import form
from z3c.form import button
from zope import component
from zope import interface

from collective.rcse.settings import IPersonalPreferences
from collective.rcse.settings import getUserSettings
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

    @button.buttonAndHandler(_(u"Save"), name="save")
    def handleApply(self, action):
        settings = getUserSettings(self.context)
        #@TODO


class PersonalPreferencesFormWrapper(FormWrapper):
    form = PersonalPreferencesForm
