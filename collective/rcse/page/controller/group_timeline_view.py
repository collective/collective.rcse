from Products.CMFCore.utils import getToolByName

from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.page.controller.group_base import BaseView

_ = RCSEMessageFactory


class TimelineView(BaseView):
    """Timeline view"""

    def __call__(self):
        self.update()
        return self.index()

    def __init__(self, context, request):
        super(TimelineView, self).__init__(context, request)
        self.plone_utils = None
        self.use_view_action = None

    def update(self):
        if self.plone_utils is None:
            self.plone_utils = getToolByName(self.context, 'plone_utils')
        if self.use_view_action is None:
            pp = getToolByName(self.context, 'portal_properties')
            self.use_view_action = pp.getProperty(
                'typesUseViewActionInListings', ()
            )
        super(TimelineView, self).update()

    @property
    def filter_type(self):
        portal_types = self.plone_utils.getUserFriendlyTypes()
        portal_types.remove("collective.rcse.group")
        return portal_types
