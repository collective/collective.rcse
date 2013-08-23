from zope import component
from collective.rcse.action import ajax
from collective.rcse.content.group import GroupSchema
from collective.rcse.i18n import _
from Products.statusmessages.interfaces import IStatusMessage


class Join(ajax.AjaxAction):
    """Request Writer local role access using collective.request.access
    or if the current group is open, just give him the role"""

    def action(self):
        #precondition
        if not GroupSchema.providedBy(self.context):
            raise ValueError("can t join something that is not a group")
        portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        member = portal_state.member()
        if member is None:
            raise ValueError("you must be authenticated")

        context_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state'
        )
        state = context_state.workflow_state()
        role = "Contributor"
        if state == "open":
            #just add the localrole
            self.context.manage_setLocalRoles(member.getId(), [role])
            msg = _(u"You have joined this group")
        else:
            #create a request
            manager = self.context.restrictedTraverse("@@request_manager")
            request = manager.create()
            request.role = role
            manager.add(request)
            msg = _(u"You have request access to this group. Please wait for an administrator to validate it")

        self.request.response.redirect(context_state.view_url())
        status = IStatusMessage(self.request)
        status.add(msg)


class Quit(ajax.AjaxAction):
    """Quit this group"""
    def action(self):
        if not GroupSchema.providedBy(self.context):
            raise ValueError("can t join something that is not a group")
        portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        member = portal_state.member()
        if member is None:
            raise ValueError("you must be authenticated")

        context_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state'
        )
        self.context.manage_delLocalRoles([member.getId()])
        msg = _(u"You have quit this group")
        self.request.response.redirect(context_state.view_url())
        status = IStatusMessage(self.request)
        status.add(msg)
