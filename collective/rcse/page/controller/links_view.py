from plone.supermodel import model
from zope import interface
from zope import schema
from zope import component
from z3c.form import button

from collective.rcse.i18n import _
from collective.rcse.page.controller import group_base
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView

CONTENT_TYPE = 'Link'


class AddFormSchema(model.Schema):
    """Add form"""
    title = schema.TextLine(title=_(u"Title"))
    description = schema.Text(
        title=_(u"Description"),
    )
    url = schema.TextLine(title=_(u"URL"))


class AddFormAdapter(object):
    interface.implements(AddFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context
        self.title = None
        self.url = None
        self.description = None


class AddForm(group_base.BaseAddForm):
    schema = AddFormSchema
    msg_added = _(u"Link added")
    label = _(u"Add link")
    CONTENT_TYPE=CONTENT_TYPE

    @button.buttonAndHandler(_(u"Add link"))
    def handleAdd(self, action):
        group_base.BaseAddForm.handleAdd(self, action)


class LinksView(group_base.BaseAddFormView):
    """A filterable timeline"""
    filter_type = ["Link"]
    form = AddForm


class NavigationRootLinksView(LinksView, NavigationRootBaseView):
    def update(self):
        LinksView.update(self)
        NavigationRootBaseView.update(self)
