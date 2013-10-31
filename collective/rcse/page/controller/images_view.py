from zope import interface
from zope import schema
from zope import component
from z3c.form import button

from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.uuid.interfaces import IUUID

from collective.rcse.content.group import get_group
from collective.rcse.i18n import _
from collective.rcse.page.controller import group_base
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView

CONTENT_TYPE = "Image"


class AddFormSchema(group_base.BaseAddFormSchema):
    """Add form"""
    image = NamedBlobImage(
        title=_(u"Image"),
        description=_(u"Please put an image file here"))
    title = schema.TextLine(
        title=_(u"Title"),
        required=False,
        )
    description = schema.Text(
        title=_(u"Description"),
        required=False
    )


class AddFormAdapter(object):
    interface.implements(AddFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context
        self.image = None
        self.title = None
        self.description = None
        self.where = None
        group = get_group(context)
        if group:
            self.where = IUUID(group)


class AddForm(group_base.BaseAddForm):
    schema = AddFormSchema
    CONTENT_TYPE = CONTENT_TYPE
    msg_added = _(u"Image added")
    label = _(u"Add image")

    @button.buttonAndHandler(_(u"Add Image"))
    def handleAdd(self, action):
        group_base.BaseAddForm.handleAdd(self, action)


class ImagesView(group_base.BaseAddFormView):
    """A filterable timeline"""
    filter_type = [CONTENT_TYPE]
    form = AddForm


class NavigationRootImagesView(ImagesView, NavigationRootBaseView):
    def update(self):
        ImagesView.update(self)
        NavigationRootBaseView.update(self)
