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

CONTENT_TYPE = "News Item"


class AddFormSchema(group_base.BaseAddFormSchema):
    """Add form"""
    title = schema.TextLine(title=_(u"Title"))
    description = schema.Text(
        title=_(u"Description"),
        required=False
    )
    image = NamedBlobImage(
        title=_(u"Image"),
        description=_(u"Please put an image file here"),
        required=False
    )


class AddFormAdapter(object):
    interface.implements(AddFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context
        self.title = None
        self.image = None
        self.description = None
        self.where = None
        group = get_group(context)
        if group:
            self.where = IUUID(group)


class AddForm(group_base.BaseAddForm):
    schema = AddFormSchema
    CONTENT_TYPE = CONTENT_TYPE
    msg_added = _(u"Blog post added")
    label = _(u"Add blog")

    @button.buttonAndHandler(_(u"Add Blog"))
    def handleAdd(self, action):
        group_base.BaseAddForm.handleAdd(self, action)


class BlogView(group_base.BaseAddFormView):
    """A filterable blog view"""
    filter_type = [CONTENT_TYPE]
    form = AddForm


class NavigationRootBlogView(BlogView, NavigationRootBaseView):
    def update(self):
        BlogView.update(self)
        NavigationRootBaseView.update(self)
