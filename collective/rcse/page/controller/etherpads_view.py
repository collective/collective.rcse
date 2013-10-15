from plone.supermodel import model
from zope import interface
from zope import schema
from zope import component
from z3c.form import button

from collective.rcse.content.group import get_group
from collective.rcse.i18n import _
from collective.rcse.page.controller import group_base
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView

CONTENT_TYPE = 'collective.rcse.etherpad'


class AddFormSchema(group_base.BaseAddFormSchema):
    """Add form"""
    title = schema.TextLine(title=_(u"Title"))
    description = schema.Text(
        title=_(u"Description"),
    )


class AddFormAdapter(object):
    interface.implements(AddFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context
        self.title = None
        self.description = None
        self.where = None
        group = get_group(context)
        if group:
            self.where = IUUID(group)


class AddForm(group_base.BaseAddForm):
    schema = AddFormSchema
    msg_added = _(u"Etherpad added")
    label = _(u"Add Etherpad")
    CONTENT_TYPE=CONTENT_TYPE

    @button.buttonAndHandler(_(u"Add etherpad"))
    def handleAdd(self, action):
        group_base.BaseAddForm.handleAdd(self, action)


class EtherpadsView(group_base.BaseAddFormView):
    """A filterable timeline"""
    filter_type = [CONTENT_TYPE]
    form = AddForm


class NavigationRootEtherpadsView(EtherpadsView, NavigationRootBaseView):
    def update(self):
        EtherpadsView.update(self)
        NavigationRootBaseView.update(self)
