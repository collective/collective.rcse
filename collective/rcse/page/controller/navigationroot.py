from zope import component
from Products.Five.browser import BrowserView


class NavigationRootBaseView(BrowserView):
    def update(self):
        self.query["path"] = '/'.join(self.context.getPhysicalPath())
        self.portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        self.query["group_watchers"] = self.portal_state.member().getId()
