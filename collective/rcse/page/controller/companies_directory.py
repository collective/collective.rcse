from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView


class CompaniesDirectoryView(BrowserView):
    """View for the companies directory."""

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
            self.catalog = getToolByName(self.context, 'portal_catalog')
        if self.directory_url is None:
            portal_url = getToolByName(self.context, 'portal_url')
            root = portal_url.getPortalObject()
            root_url = '/'.join(root.getPhysicalPath())
            self.directory_url = '%s/companies_directory' % root_url

    def makeQuery(self):
        self.query = {
#            'path': {'query': self.directory_url, 'depth': 1},
#            'sort_on': 'sortable_title',
#            'sort_order': 'ascending',
#            'sort_limit': 20,
            'portal_type': 'collective.rcse.company'
            }

    def getCompanies(self, batch=True, b_size=10, b_start=0):
#        brains = self.catalog(**self.query)
        results = []
        for id, item in self.context.contentItems():
                results.append(item)
        return results
