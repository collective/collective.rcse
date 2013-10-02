from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView


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
#            'path': {'query': self.directory_url, 'depth': 1},
            #'sort_on': 'sortable_title',
            #'sort_order': 'ascending',
            #'sort_limit': 20,
            'portal_type': 'collective.rcse.member',
            #'review_state': 'enabled',
            }

    def getMembers(self, review_state="enabled"):
        self.query.update({'review_state': review_state})
        results = self.catalog(**self.query)
        return self._results2info(results)

    def _results2info(self, brains):
        userids = [brain.getUserId for brain in brains]

        def getInfo(userid):
            person_view = self.context.restrictedTraverse('get_memberinfo')
            person_view(userid)
            return {
                "userid": userid,
                "dataid": person_view.get_membrane().getId(),
                "url": person_view.url,
                "photo": person_view.photo(),
                "email": person_view.email,
                "first_name": person_view.first_name,
                "last_name": person_view.last_name,
                "company": person_view.company,
                "function": person_view.function,
                "city": person_view.city,
            }
        info = map(getInfo, userids)
        return info

    def canManageUsers(self):
        usersDirectory = self.context.restrictedTraverse('users_directory')
        sm = getSecurityManager()
        return sm.checkPermission(ReviewPortalContent, usersDirectory)
