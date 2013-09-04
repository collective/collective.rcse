from collective.rcse.page.controller.group_base import BaseView
from zope import interface
from zope import schema
from zope import component
from plone.namedfile.field import NamedBlobImage
from plone.autoform.form import AutoExtensibleForm
from z3c.form import form, field, button
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from collective.rcse.i18n import _
from Products.statusmessages.interfaces import IStatusMessage

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

    @button.buttonAndHandler(_(u"Add"))
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        self.doAdd(data)

    def doAdd(self):
        import pdb;pdb.set_trace()

        IStatusMessage(self.request).add(_(u"Image added"))
        referer = self.request.get("HTTP_REFERER")
        if not referer:
            referer = self.context.absolute_url()
        self.request.response.redirect(referer)

class ImagesView(BaseView, FormWrapper):
    """A filterable timeline"""
    filter_type = ["Image"]
    form = AddImageForm

    def __init__(self, context, request):
        BaseView.__init__(self, context, request)
        FormWrapper.__init__(self, context, request)

    def update(self):
        BaseView.update(self)
        FormWrapper.update(self)
