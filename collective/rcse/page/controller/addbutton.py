from Products.Five.browser import BrowserView
from plone.app.z3cform import layout
from zope import interface
from zope import schema
from zope import component
from z3c.form import form

from collective.rcse.i18n import _
from collective.rcse.content.group import get_group
from plone.uuid.interfaces import IUUID
from plone.autoform.form import AutoExtensibleForm


class AddFormSchema(interface.Interface):
    what = schema.Choice(
        title=_(u"What"),
        vocabulary="plone.app.vocabularies.UserFriendlyTypes",
        default="collective.rcse.group"
    )
    where = schema.Choice(
        title=_(u"Where"),
        description=_(u"Warning, only groups can be added into Home"),
        vocabulary="collective.rcse.vocabulary.groups_with_home"
    )


class AddFormAdapter(object):
    interface.implements(AddFormSchema)
    component.adapts(interface.Interface)
    def __init__(self, context):
        self.what = "collective.rcse.group"
        self.where = None
        group = get_group(context)
        if group:
            self.where = IUUID(group)


class AddForm(AutoExtensibleForm, form.Form):
    schema = AddFormSchema
    form_name = 'add_content'


class AddButton(layout.FormWrapper):
    """Add button"""
    form = AddForm

    def update(self):
        super(AddButton, self).update()
