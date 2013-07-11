from AccessControl.unauthorized import Unauthorized
from collective.rcse.i18n import RCSEMessageFactory
from plone.uuid.interfaces import IUUID
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

_ = RCSEMessageFactory


class TimelineView(BrowserView):
    """Timeline view"""

    def __call__(self):
        self.update()
        return self.index()

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.portal_catalog = None
        self.context_path = None
        self.query = None
        self.results = []
        self.plone_utils = None
        self.use_view_action = None

    def update(self):
        if self.portal_catalog is None:
            self.portal_catalog = getToolByName(self.context, 'portal_catalog')
        if self.plone_utils is None:
            self.plone_utils = getToolByName(self.context, 'plone_utils')
        if self.context_path is None:
            self.context_path = '/'.join(self.context.getPhysicalPath())
        if self.use_view_action is None:
            pp = getToolByName(self.context, 'portal_properties')
            self.use_view_action = pp.getProperty(
                'typesUseViewActionInListings', ()
            )
        if self.query is None:
            portal_types = self.plone_utils.getUserFriendlyTypes()
            portal_types.remove("collective.rcse.group")
            self.query = {
                "path": {'query': self.context_path, 'depth': 1},
                "sort_on": "modified",
                "sort_order": "reverse",
                "sort_limit": 20,
                "portal_type": portal_types,
            }
            dofilter = self.request.get('filter', False)
            if dofilter:
                text = self.request.get('SearchableText', None)
                if text is not None:
                    self.query["SearchableText"] = text
                ptype = self.request.get('portal_type', None)
                if ptype is not None:
                    self.query["portal_type"] = ptype

    def get_content(self, batch=True, b_size=10, b_start=0):
        results = self.portal_catalog(self.query)
        if batch:
            results = Batch(results, b_size, b_start)
        return results
