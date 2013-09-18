from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope import component
from Acquisition import aq_parent



class BreadCrumb(BrowserView):
    """rcse bread crumb give a list of group at root / group under / ..."""
    filter = {}

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.path = self.context.getPhysicalPath()
        self.path_str = "/".join(self.context.getPhysicalPath())
        self.context_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state'
        )
        self.portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        self.navroot = self.portal_state.navigation_root()
        self.navroot_path = self.navroot.getPhysicalPath()
        parents_ids = self.path[len(self.navroot_path):]

        #the breadcrumb let you select two levels of groups

        self.parents_info = []
        query1 = {"path": {"query": '/'.join(self.navroot_path), "depth": 1},
                  "portal_type": "collective.rcse.group"}
        brains = self.catalog(**query1)
        parents = self.get_brain_info(brains)
        self.parents_info.append(parents)
        self.parent_url = None

        #level2.
        #FIXME: il faut voir au niveau du parents_ids.
        if len(parents_ids) > 0:  #context is in a group
            self.parent_url = self.context.aq_inner.aq_parent.absolute_url()
            #We add Back to current group in the list
            path = '/'.join(self.navroot_path + parents_ids[:1])
            query2 = {"path": {"query": path, "depth": 1}, 
                      "portal_type": "collective.rcse.group"}
            brains = self.catalog(**query2)
            if brains:
                parents = self.get_brain_info(brains)
                self.parents_info.append(parents)

    def get_brain_info(self, brains):
        def get(brain):
            current = False
            if brain.getPath() in self.path_str:
                current = True
            return {"id": brain.getId,
                    "title": brain.Title,
                    "description": brain.Description,
                    "url": brain.getURL,
                    "portal_type": brain.portal_type,
                    "current": current}
        return map(get, brains)

    def has_current(self, parents):
        for parent in parents:
            if parent["current"]:
                return True
        return False
