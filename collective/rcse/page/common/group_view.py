from Products.Five.browser import BrowserView
from collective.rcse.i18n import RCSEMessageFactory
from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID

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

    def update(self):
        if self.portal_catalog is None:
            self.portal_catalog = getToolByName(self.context, 'portal_catalog')
        if self.context_path is None:
            self.context_path = '/'.join(self.context.getPhysicalPath())
        if self.query is None:
            iface = "collective.rcse.content.common.RCSEContent"
            self.query = {
                "path": {'query': self.context_path, 'depth': 1},
                "sort_on": "modified",
                "sort_order": "reverse",
                "sort_limit": 20,
                "object_provides": iface,
            }
            dofilter = self.request.get('filter', False)
            if dofilter:
                text = self.request.get('SearchableText', None)
                if text is not None:
                    self.query["SearchableText"] = text
                ptype = self.request.get('portal_type', None)
                if ptype is not None:
                    self.query["portal_type"] = ptype

    def get_content(self):
        if not self.results:
            brains = self.portal_catalog(self.query)
            self.results = map(self.get_brain_info, brains)
        return self.results

    def get_brain_info(self, brain):
        return brain.getURL()


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
