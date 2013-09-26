from zope import interface
from zope import schema
from zope import component
from z3c.form import button

from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.app.event.dx.behaviors import IEventBasic

from collective.rcse.i18n import _
from collective.rcse.page.controller import group_base
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView

CONTENT_TYPE = "collective.rcse.event"


class AddFormSchema(IEventBasic):
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
        self.start = None
        self.end = None
        self.whole_day = None
        self.open_end = None
        self.timezone = None


class AddForm(group_base.BaseAddForm):
    schema = AddFormSchema
    CONTENT_TYPE = CONTENT_TYPE
    msg_added = _(u"Event added")
    label = _(u"Add event")

    @button.buttonAndHandler(_(u"Add event"))
    def handleAdd(self, action):
        group_base.BaseAddForm.handleAdd(self, action)


class EventsView(group_base.BaseAddFormView):
    """A filterable blog view"""
    filter_type = [CONTENT_TYPE]
    form = AddForm


class NavigationRootEventsView(EventsView, NavigationRootBaseView):
    def update(self):
        EventsView.update(self)
        NavigationRootBaseView.update(self)
