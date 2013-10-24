from zope import component
from collective.rcse.action import ajax
from collective.rcse.content.group import GroupSchema
from collective.rcse.content.proxygroup import ProxyGroupSchema
from collective.rcse.i18n import _
from Products.statusmessages.interfaces import IStatusMessage


class Join(ajax.AjaxAction):
    """Request Writer local role access using collective.request.access
    or if the current group is open, just give him the role"""
    kind = GroupSchema
    def get_group(self):
        return self.context

    def action(self):
        #precondition
        if not self.kind.providedBy(self.context):
            raise ValueError("can t join something that is not a group")
        group = self.get_group()
        portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        member = portal_state.member()
        if member is None:
            raise ValueError("you must be authenticated")

        group_state = component.getMultiAdapter(
            (group, self.request),
            name=u'plone_context_state'
        )
        state = group_state.workflow_state()
        role = "Contributor"
        if state == "open":
            #just add the localrole
            group.manage_setLocalRoles(member.getId(), [role])
            msg = _(u"You have joined this group")
        elif state == "moderated":
            #You are supposed to already have view context to be here
            manager = group.restrictedTraverse("@@request_manager")
            request = manager.create()
            request.role = role
            manager.add(request)
            msg = _(u"You have request access to this group. Please wait for an administrator to validate it")

        self.request.response.redirect(self.context.absolute_url())
        status = IStatusMessage(self.request)
        status.add(msg)


class Quit(ajax.AjaxAction):
    """Quit this group"""
    kind = GroupSchema
    def get_group(self):
        return self.context

    def action(self):
        if not self.kind.providedBy(self.context):
            raise ValueError("can t join something that is not a group")
        group = self.get_group()
        portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        member = portal_state.member()
        if member is None:
            raise ValueError("you must be authenticated")

        group_state = component.getMultiAdapter(
            (group, self.request),
            name=u'plone_context_state'
        )
        group.manage_delLocalRoles([member.getId()])
        msg = _(u"You have quit this group")
        url = group.aq_parent.absolute_url()
        self.request.response.redirect(url)
        status = IStatusMessage(self.request)
        status.add(msg)


class ProxyJoin(Join):
    kind = ProxyGroupSchema
    def get_group(self):
        return self.context


class ProxyQuit(Quit):
    kind = ProxyGroupSchema
    def get_group(self):
        return self.context
