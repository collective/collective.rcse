from Products.CMFPlone.utils import getToolByName

from collective.rcse.page.controller.group_base import BaseView


class FavoritesView(BaseView):
    """A filterable timeline"""

    def __init__(self, context, request):
        super(FavoritesView, self).__init__(context, request)
        self.mtool = None

    def update(self):
        super(FavoritesView, self).update()
        if self.mtool is None:
            self.mtool = getToolByName(self.context, 'portal_membership')
        username = self.mtool.getAuthenticatedMember().getUserName()
        self.query['favoritedby'] = username
