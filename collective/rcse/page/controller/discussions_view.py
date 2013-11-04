from zope import component
from zope import interface
from zope import schema
from z3c.form import form, field, button

from Products.CMFPlone import PloneMessageFactory
from Products.CMFPlone.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.autoform.form import AutoExtensibleForm
from plone.dexterity import utils
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from plone.uuid.interfaces import IUUID

from collective.rcse.content.group import get_group
from collective.rcse.i18n import _
from collective.rcse.page.controller import group_base
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView


CONTENT_TYPE = "collective.rcse.discussion"


class AddFormSchema(group_base.BaseAddFormSchema):
    """Add form"""
    title = schema.TextLine(title=PloneMessageFactory(u"Title"))
    description = schema.Text(title=_(u"Subject"))
    file = NamedBlobFile(title=_(u"Attachment"),
                         required=False)


class AddFormAdapter(object):
    interface.implements(AddFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context
        self.image = None
        self.description = ''
        self.where = None
        self.file = None
        group = get_group(context)
        if group:
            self.where = IUUID(group)


class AddForm(group_base.BaseAddForm):
    schema = AddFormSchema
    CONTENT_TYPE = CONTENT_TYPE
    msg_added = _(u"Discussion added")
    label = _(u"Add Discussion")

    @button.buttonAndHandler(_(u"Add Discussion"))
    def handleAdd(self, action):
        group_base.BaseAddForm.handleAdd(self, action)


class DiscussionsView(group_base.BaseAddFormView):
    """A filterable timeline"""
    filter_type = [CONTENT_TYPE]
    form = AddForm


class NavigationRootDiscussionsView(DiscussionsView, NavigationRootBaseView):

    def update(self):
        DiscussionsView.update(self)
        NavigationRootBaseView.update(self)
