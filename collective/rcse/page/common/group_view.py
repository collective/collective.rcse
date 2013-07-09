from Products.Five.browser import BrowserView
from collective.rcse.i18n import RCSEMessageFactory
from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.PloneBatch import Batch

_ = RCSEMessageFactory


class GroupView(BrowserView):
    """default view"""

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
            self.query = {
                "path": {'query': self.context_path, 'depth': 1},
                "sort_on": "modified",
                "sort_order": "reverse",
                "sort_limit": 20,
                "portal_types": portal_types,
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
        results = map(self.get_brain_info, results)
        if batch:
            results = Batch(results, b_size, b_start)
        return results

    def get_brain_info(self, brain):
        url = brain.getURL()
        if brain.portal_type in self.use_view_action:
            url = url + '/view'
        return url


class GroupTileView(BrowserView):
    """generic view to display a tile in a group"""

    def __call__(self):
        self.update()
        return self.index()

    def __init__(self, context, request):
        super(GroupTileView, self).__init__(context, request)
        self.membership = None
        self.portal_url = None
        self.tileid = None
        self.group = None
        self.group_url = None
        self.group_title = None
        self.effective_date = None

    def update(self):
        if self.membership is None:
            self.membership = getToolByName(self.context, "portal_membership")
        if self.portal_url is None:
            self.portal_url = getToolByName(self.context, 'portal_url')()
        if self.tileid is None:
            self.tileid = IUUID(self.context)
        if self.group is None:
            self.group = self.context.aq_inner.aq_parent
        if self.group_url is None:
            self.group_url = self.group.absolute_url()
        if self.group_title is None:
            self.group_title = self.group.Title()
        if self.effective_date is None:
            self.effective_date = self.get_effective_date()

    def get_content(self):
        return self.context.restrictedTraverse('tile_view')()

    def get_effective_date(self):
        effective = None
        if self.context.effective_date is not None:
            effective = self.context.effective_date
        elif self.context.modification_date is not None:
            effective = self.context.modification_date
        elif self.context.creation_date is not None:
            effective = self.context.creation_date

        if effective is not None:
            return effective.strftime("%d-%m-%Y")
        return ""
