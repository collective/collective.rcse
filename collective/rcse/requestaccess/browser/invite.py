from plone.autoform.form import AutoExtensibleForm
from z3c.form import form, button
from zope import component
from zope import schema
from zope import interface
from plone.supermodel import model
from Products.statusmessages.interfaces import IStatusMessage
from plone.z3cform.layout import FormWrapper
from collective.requestaccess.i18n import _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class InvitationFormSchema(model.Schema):
#    userid = schema.ASCIILine(title=_(u"User ID"))
    userid = schema.Choice(
        title=_(u"User ID"),
        vocabulary="plone.app.vocabularies.Users"
    )
    role = schema.Choice(
        title=_(u"Role"),
        vocabulary="collective.requestaccess.vocabulary.roles"
    )


class InvitationFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(InvitationFormSchema)

    def __init__(self, context):
        self.context = context
        self.role = None
        self.userid = None


class InvitationForm(AutoExtensibleForm, form.Form):
    schema = InvitationFormSchema
    enableCSRFProtection = True

    @button.buttonAndHandler(_(u"Propose access"))
    def proposeAccess(self, action):
        data, errors = self.extractData()
        status = IStatusMessage(self.request)
        self.manager = self.context.restrictedTraverse("request_manager")
        request = self.manager.create()
        request.userid = data["userid"]
        request.role = data["role"]
        request.rtype = "invitation"
        if self.manager.add(request):
            status.add(_(u"Invitation sent"))
        else:
            status.add(_(u"Invitation or request already exists."),
                       type='error')
        self.request.response.redirect(self.context.absolute_url())

    @property
    def label(self):
        return _(u"Propose access on ${title}",
                 mapping={"title": self.context.Title().decode('utf-8')})


class InvitationFormWrapper(FormWrapper):
    form = InvitationForm
    index = ViewPageTemplateFile("templates/add_invite_form_view.pt")

#
# class AcceptInvitationForm(AutoExtensibleForm, form.Form):
#     schema = model.Schema
#     enableCSRFProtection = True
#
#     @button.buttonAndHandler(_(u"Accept access"))
#     def acceptAccess(self, action):
#         data, errors = self.extractData()
#         status = IStatusMessage(self.request)
#         self.manager = self.context.restrictedTraverse("request_manager")
#         self.manager.validate(self.context.id)
#         status.add(_(u"Invitation accepted"))
#         url = self.context.absolute_url() + '/@@my_requests_view'
#         self.request.response.redirect(url)
