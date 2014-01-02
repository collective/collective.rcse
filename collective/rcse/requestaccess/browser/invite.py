from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from plone.directives import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import form, button
from z3c.form.browser.select import SelectFieldWidget
from zope import component
from zope import schema
from zope import interface

from collective.requestaccess.i18n import _


class InvitationFormSchema(model.Schema):
#    userid = schema.ASCIILine(title=_(u"User ID"))
    directives.widget('userids', SelectFieldWidget, multiple="multiple")
    userids = schema.List(
        title=_(u"Users"),
        value_type=schema.Choice(
            vocabulary="collective.rcse.vocabulary.members"
        )
    )


class InvitationFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(InvitationFormSchema)

    def __init__(self, context):
        self.context = context
        self.userids = None


class InvitationForm(AutoExtensibleForm, form.Form):
    schema = InvitationFormSchema
    enableCSRFProtection = True

    @button.buttonAndHandler(_(u"Propose access"))
    def proposeAccess(self, action):
        data, errors = self.extractData()
        status = IStatusMessage(self.request)
        self.manager = self.context.restrictedTraverse("request_manager")
        validated = []
        for userid in data['userids']:
            request = self.manager.create()
            request.userid = userid
            request.role = "Contributor"
            request.rtype = "invitation"
            res = self.manager.add(request)
            validated.append(res)
        if False in validated:
            status.add(_(u"Invitation or request already exists."))
        else:
            status.add(_(u"Invitation sent"))
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
