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
        if self.context.portal_type == "collective.rcse.group":
            parents_ids = parents_ids[:-1]
        current_path = "/".join(self.navroot_path)
        self.parents_path = [current_path]
        for parent_id in parents_ids:
            current_path = "%s/%s" % (current_path, parent_id)
            self.parents_path.append(current_path)

        current = self.context.aq_inner
        current_path = "/".join(current.getPhysicalPath())
        self.parents = {current_path: current}
        while current_path != "/".join(self.navroot_path):
            current = aq_parent(current)
            current_path = "/".join(current.getPhysicalPath())
            self.parents[current_path] = current

        self.parents_info = []
        for path in self.parents_path:
            query = {"path": {"query": path, "depth": 1}, 
                     "portal_type": "collective.rcse.group"}
            query.update(self.filter)
            brains = self.catalog(**query)
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
