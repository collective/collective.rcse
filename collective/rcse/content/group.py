from Products.Five.browser import BrowserView
from collective.rcse.i18n import RCSEMessageFactory
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.uuid.interfaces import IUUID

_ = RCSEMessageFactory


class GroupView(BrowserView):
    """default view"""
    index = ViewPageTemplateFile("templates/group_view.pt")

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.portal_catalog = getToolByName(self.context, 'portal_catalog')
        self.context_path = '/'.join(self.context.getPhysicalPath())
        self.query = {"path": {'query': self.context_path, 'depth': 1},
                      "sort_on": "effective",
                      "sort_order": "reverse",
                      "sort_limit": 20}
        dofilter = self.request.get('filter', False)
        if dofilter:
            text = self.request.get('SearchableText', None)
            if text is not None:
                self.query["SearchableText"] = text
            ptype = self.request.get('portal_type', None)
            if ptype is not None:
                self.query["portal_type"] = ptype
        self.results = []

    def get_content(self):
        if not self.results:
            brains = self.portal_catalog(self.query)
            self.results = map(self.get_brain_info, brains)
        return self.results

    def get_brain_info(self, brain):
        return brain.getURL()


class GroupTileView(BrowserView):
    index = ViewPageTemplateFile("templates/group_tile_view.pt")

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.membership = getToolByName(self.context, "portal_membership")
        self.portal_url = getToolByName(self.context, 'portal_url')()
        self.tileid = IUUID(self.context)
        self.author_id = self.context.Creator()
        self.author = self.membership.getMemberById(self.author_id)
        self.author_name = self.author.getProperty('fullname')
        self.author_url = self.portal_url + '/author/' + self.author_id
        portrait = self.membership.getPersonalPortrait(self.author_id)
        if portrait:
            self.portrait = portrait.absolute_url()
        else:
            path = '/++resource++collective.rcse/defaultUser.png'
            self.portrait = self.portal_url + path
        self.group = self.context.aq_inner.aq_parent
        self.group_url = self.group.absolute_url()
        self.group_title = self.group.Title()

    def get_content(self):
        return self.context.restrictedTraverse('tile_view')()
