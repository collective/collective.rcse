from collective.requestaccess.i18n import _
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import form, button
from zope import component
from zope import schema
from zope import interface


class RequestView(BrowserView):
    """request view"""
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_state = None

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        if self.portal_state is None:
            self.portal_state = component.getMultiAdapter(
                (self.context, self.request),
                name="plone_portal_state",
            )


class AddRequestFormSchema(model.Schema):
    role = schema.Choice(
        title=_(u"Role"),
        vocabulary="collective.requestaccess.vocabulary.roles"
    )


class AddRequestFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(AddRequestFormSchema)

    def __init__(self, context):
        self.context = context
        self.role = None


class AddRequestForm(AutoExtensibleForm, form.Form):
    schema = AddRequestFormSchema
    enableCSRFProtection = True

    @button.buttonAndHandler(_(u"Request access"))
    def requestAccess(self, action):
        data, errors = self.extractData()
        role = data.get('role')
        manager = self.context.restrictedTraverse("@@request_manager")
        request = manager.create()
        request.role = role
        status = IStatusMessage(self.request)
        if manager.add(request):
            msg = _(u"Your request has been saved. It's now under review")
            status.add(msg)
        else:
            status.add(_(u"Invitation or request already exists."),
                       type='error')
        self.request.response.redirect(self.context.absolute_url())

    @property
    def label(self):
        return _(u"Request access on ${title}",
                 mapping={"title": self.context.Title().decode('utf-8')})


class AddRequestFormView(FormWrapper):
    form = AddRequestForm
    index = ViewPageTemplateFile("templates/add_request_form_view.pt")


class ValidationRequestFormSchema(model.Schema):
    requestaccessid = schema.ASCIILine(title=_(u"Request ID"))


class ValidationRequestFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(ValidationRequestFormSchema)

    def __init__(self, context):
        self.context = context
        self.requestaccessid = None  # filled by the viewlet


class ValidationRequestForm(AutoExtensibleForm, form.Form):
    schema = ValidationRequestFormSchema
    enableCSRFProtection = True

    @button.buttonAndHandler(_(u"Validate access"))
    def validateAccess(self, action):
        data, errors = self.extractData()

        rid = data.get("requestaccessid")
        status = IStatusMessage(self.request)
        if rid is None:
            status.add(_(u"You must provide a request ID"))
        else:
            self.manager = self.context.restrictedTraverse("request_manager")
            self.manager.validate(rid)
            status.add(_(u"The request has been validated"))
        if not hasattr(self, 'next_url'):
            self.next_url = self.context.absolute_url()
        self.request.response.redirect(self.next_url)

    @button.buttonAndHandler(_(u"Refuse access"))
    def RefuseAccess(self, action):
        data, errors = self.extractData()

        rid = data.get("requestaccessid")
        status = IStatusMessage(self.request)
        if rid is None:
            status.add(_(u"You must provide a request ID"))
        else:
            self.manager = self.context.restrictedTraverse("request_manager")
            self.manager.refuse(rid)
            status.add(_(u"The request has been refused"))
        self.request.response.redirect(self.next_url)


class ValidationInvitationForm(AutoExtensibleForm, form.Form):
    schema = ValidationRequestFormSchema
    enableCSRFProtection = True

    def getContent(self):
        return {}

    @button.buttonAndHandler(_(u"Accept access"))
    def acceptAccess(self, action):
        data, errors = self.extractData()

        rid = data.get("requestaccessid")
        status = IStatusMessage(self.request)
        if rid is None:
            status.add(_(u"You must provide a request ID"))
        else:
            self.manager = self.context.restrictedTraverse("request_manager")
            self.manager.validate(rid)
            status.add(_(u"You have accepted the invitation"))
        self.request.response.redirect(self.next_url)

    @button.buttonAndHandler(_(u"Decline access"))
    def declineAccess(self, action):
        data, errors = self.extractData()

        rid = data.get("requestaccessid")
        status = IStatusMessage(self.request)
        if rid is None:
            status.add(_(u"You must provide a request ID"))
        else:
            self.manager = self.context.restrictedTraverse("request_manager")
            self.manager.refuse(rid)
            status.add(_(u"You have declined access"))
        self.request.response.redirect(self.next_url)


class CancelRequestFormSchema(model.Schema):
    requestaccessid = schema.ASCIILine(title=_(u"Request ID"))


class CancelRequestFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(CancelRequestFormSchema)

    def __init__(self, context):
        self.context = context
        self.requestaccessid = None


class CancelRequestForm(AutoExtensibleForm, form.Form):
    schema = CancelRequestFormSchema
    enableCSRFProtection = True

    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        if self.request.response.getStatus() in (302, 303):
            return
        data, errors = self.extractData()
        self.manager = self.context.restrictedTraverse("request_manager")
        rid = data.get("requestaccessid")
        self.manager.remove(rid)
        status = IStatusMessage(self.request)
        message = _(u"Your request has been canceled")
        status.add(message)
        self.request.response.redirect(self.next_url)
