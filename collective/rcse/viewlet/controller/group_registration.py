from Acquisition import aq_inner, aq_parent
from plone.app.layout.viewlets.common import ViewletBase


class GroupRegistration(ViewletBase):
    """Let the user join / quit a group"""

    def update(self):
        ViewletBase.update(self)
        context = aq_inner(self.context)
        while context.portal_type != "collective.rcse.group":
            if context.portal_type == "Plone Site":
                break
            context = aq_parent(context)
            if context.portal_type == "Plone Site":
                break
        if context.portal_type == "collective.rcse.group":
            self.group = context
        else:
            self.group = None
        self.member = self.portal_state.member()
        if self.member is not None and self.group is not None:
            self.memberid = self.member.getId()
            getroles = self.group.manage_getUserRolesAndPermissions
            self.roles = getroles(self.memberid)
            self.isOwner = self.hasRole("Owner")
#            owner = self.group.getOwner()
#            if owner:
#                self.isOwner = self.memberid == owner.getId()
            self.isManager = self.hasRole("Manager")
            self.isSiteAdmin = self.hasRole("Site Administrator")
            self.isContributor = self.hasRole("Contributor")

    def group_url(self):
        if self.group:
            return self.group.absolute_url()

    def should_render(self):
        if not self.member or not self.group:
            return False
        return not self.isOwner and not self.isManager and not self.isSiteAdmin

    def can_join(self):
        """You can join a group if:
         - You are not already a member (Contributor local role)
         - You are not the owner of the group (Owner local role)
         - You are not administrator
        """
        if not self.group or not self.member:
            return False
        if self.isContributor or self.isOwner or self.isManager or self.isSiteAdmin:
            return False
        return True

    def can_quit(self):
        """You can quit a group if:
         - You are a member of the group
         - You are not the owner of the group
         - You are not administrator
         """
        if not self.group or not self.member:
            return False
        if self.isOwner or self.isManager or self.isSiteAdmin:
            return False
        if self.isContributor:
            return True
        return False

    def hasRole(self, role):
        hasRole = False
        for kind in ("roles", "roles_in_context"):
            hasRole = role in self.roles[kind]
            if hasRole:
                break
        return hasRole
