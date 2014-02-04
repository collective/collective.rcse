from Products.Five.browser import BrowserView
from zope import component

from collective.rcse.content.group import get_group
from collective.rcse.icons import getType


class FilterButtonView(BrowserView):
    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
            )

    def group_url(self):
        group = get_group(self.context)
        if group is None:
            group_url = self.portal_state.navigation_root_url()
            if not group_url.endswith('/home'):
                group_url += '/home'
        else:
            group_url = group.absolute_url()
        return group_url

    def get_icon(self, term):
        return getType(term)
