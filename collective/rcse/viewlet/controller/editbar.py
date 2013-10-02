from Acquisition import aq_inner, aq_parent
from plone.app.layout.viewlets.common import ViewletBase, ContentViewsViewlet,\
    ContentActionsViewlet
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from zope.component import getMultiAdapter
from plone.app.layout.globals.interfaces import IViewView
from zope.interface.declarations import alsoProvides
from zope.component._api import getUtility, getAdapter, queryAdapter
from zope.browsermenu.interfaces import IBrowserMenu
from plone.stringinterp.interfaces import IStringSubstitution
from Products.CMFCore.WorkflowCore import WorkflowException
from plone.uuid.interfaces import IUUID
from collective.rcse.content.group import get_group

MENUS = (
    'plone_contentmenu_actions',
    'plone_contentmenu_display',
    'plone_contentmenu_factory',
    'plone_contentmenu_workflow',
    'plone_contentmenu',
    'plone_displayviews',
)


class EditBar(ViewletBase):
    """Edit bar is a complete revamp to simplify the plone one"""
    def update(self):
        self.membership = getToolByName(self.context, 'portal_membership')
        super(EditBar, self).update()

        #MENU
        self.menus = {}
        for menu in MENUS:
            self.menus[menu] = getUtility(
                IBrowserMenu,
                name=menu,
            ).getMenuItems(self.context, self.request)
        #remove advanced workflow action if exists
        if len(self.menus["plone_contentmenu_workflow"]):
            del self.menus["plone_contentmenu_workflow"][-1]
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.object_actions = self.context_state.actions('object')

        try:
            adapter = queryAdapter(self.context,
                                   IStringSubstitution,
                                   'review_state_title')
            if adapter:
                self.review_state = adapter()
            else:
                self.review_state = None
        except WorkflowException:
            self.review_state = None

        self.object_uid = unicode(IUUID(self.context, u""))

        self.group = get_group(self.context)
        self.isGroup = self.context.portal_type in (
            "collective.rcse.group", "collective.rcse.proxygroup"
        )
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

    def isVisitor(self):
        if not self.member or not self.group:
            return False
        return not self.isOwner and not self.isManager and not self.isSiteAdmin

    def can_manage(self):
        if not self.member or not self.group:
            return False
        return self.isOwner or self.isManager or self.isSiteAdmin

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




class EditBarView(EditBar):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        return self.index()
