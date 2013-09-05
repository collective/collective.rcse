from zope import interface
from zope import schema
from zope import component
from z3c.form import form, field, button

from plone.namedfile.field import NamedBlobImage
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plone.dexterity import utils
from plone.z3cform.layout import FormWrapper

from Products.statusmessages.interfaces import IStatusMessage

from collective.rcse.i18n import _
from collective.rcse.page.controller.group_base import BaseView
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView

CONTENT_TYPE = "Image"

class AddImageFormSchema(model.Schema):
    """Add image form"""
    image = NamedBlobImage(
        title=_(u"Image"),
        description=_(u"Please put an image file here"))
    description = schema.Text(
        title=_(u"Description"),
        required=False
    )

class AddImageFormAdapter(object):
    interface.implements(AddImageFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context
        self.image = None
        self.description = None

class AddImageForm(AutoExtensibleForm, form.Form):
    schema = AddImageFormSchema
    enableCSRFProtection = True

    @button.buttonAndHandler(_(u"Add Image"))
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        self.doAdd(data)

    def doAdd(self, data):
        container = self.context
        item = utils.createContentInContainer(
            container,
            CONTENT_TYPE,
            checkConstraints=True,
            **data)

        IStatusMessage(self.request).add(_(u"Image added"))
        referer = self.request.get("HTTP_REFERER")
        if not referer:
            referer = self.context.absolute_url()
        self.request.response.redirect(referer)

class ImagesView(BaseView, FormWrapper):
    """A filterable timeline"""
    filter_type = [CONTENT_TYPE]
    form = AddImageForm

    def __init__(self, context, request):
        BaseView.__init__(self, context, request)
        FormWrapper.__init__(self, context, request)

    def update(self):
        BaseView.update(self)
        FormWrapper.update(self)


class NavigationRootImagesView(ImagesView, NavigationRootBaseView):
    def update(self):
        ImagesView.update(self)
        NavigationRootBaseView.update(self)
