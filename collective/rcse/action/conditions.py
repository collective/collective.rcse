from OFS.SimpleItem import SimpleItem
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope import component
from zope import interface
from zope import schema
from zope.component.interfaces import IObjectEvent
from zope.formlib import form

from collective.rcse.i18n import _
from collective.rcse.content.vocabularies import settings


class IPreferenceCondition(interface.Interface):
    preference = schema.Choice(
        title=_(u"Preference"),
        vocabulary=settings
        )
    condition = schema.Bool(
        title=_(u"Condition")
        )


class PreferenceCondition(SimpleItem):
    interface.implements(IPreferenceCondition, IRuleElementData)

    preference = None
    condition = True
    element = "collective.rcse.conditions.Preference"

    @property
    def summary(self):
        return _(u"Preference ${preference} is ${condition}.",
                 mapping={'preference': self.preference,
                          'condition': self.condition})


class PreferenceConditionExecutor(object):
    interface.implements(IExecutable)
    component.adapts(interface.Interface, IPreferenceCondition, IObjectEvent)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        user = self.context.restrictedTraverse('auth_memberinfo')
        user.update()
        preferences = user.get_settings()
        value = preferences.get(self.element.preference)
        return value == self.element.condition


class PreferenceConditionAddForm(AddForm):
    form_fields = form.FormFields(IPreferenceCondition)
    label = _(u"Add Preference Condition")
    description = _(u"Apply only if the user's preference match.")
    form_name = _(u"Configure element")

    def create(self, data):
        c = PreferenceCondition()
        form.applyChanges(c, self.form_fields, data)
        return c


class PreferenceConditionEditForm(EditForm):
    form_fields = form.FormFields(IPreferenceCondition)
    label = _(u"Edit Preference Condition")
    description = _(u"Apply only if the user's preference match.")
    form_name = _(u"Configure element")
