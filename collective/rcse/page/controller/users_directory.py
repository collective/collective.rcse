from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.rcse.content.member import get_members_info


class UsersDirectoryView(BrowserView):
    """View for the users directory."""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.query = {}

        self.catalog = None
        self.directory_url = None

    def __call__(self):
        self.update()
        self.makeQuery()
        return self.index()

    def update(self):
        if self.catalog is None:
            self.catalog = getToolByName(self.context, 'membrane_tool')
        if self.directory_url is None:
            portal_url = getToolByName(self.context, 'portal_url')
            root = portal_url.getPortalObject()
            root_url = '/'.join(root.getPhysicalPath())
            self.directory_url = '%s/users_directory' % root_url

    def makeQuery(self):
        self.query = {
            'sort_on': 'getId',  # because in mobile we need sorted results
            'portal_type': 'collective.rcse.member',
        }

    def getMembers(self, review_state="enabled"):
        get_members_info(self.context, review_state=review_state)

    def canManageUsers(self):
        usersDirectory = self.context.restrictedTraverse('users_directory')
        sm = getSecurityManager()
        return sm.checkPermission(ReviewPortalContent, usersDirectory)
