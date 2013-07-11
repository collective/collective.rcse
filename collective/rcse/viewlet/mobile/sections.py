from plonetheme.jquerymobile.browser.viewlets.header import GlobalSections
from collective.favoriting.browser.favoriting_view import VIEW_NAME
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase


class RCSESections(GlobalSections):
    """We can have a lots of sections so we need to split into two groups:
    * favorites sections comes first
    * watched sections comes second
    * all others comes into an autocomplete
    """
    def update(self):
        ViewletBase.update(self)
        super(RCSESections, self).update()
        favmanager = self.context.restrictedTraverse(VIEW_NAME)
        query = {"portal_type": "collective.rcse.group",
                 "sort_on": "sortable_title",
                 "sort_limit": 5}
        self.favorites = favmanager.get(query=query)
        catalog = getToolByName(self.context, 'portal_catalog')
        memberid = self.portal_state.member().getId()
        query = {"portal_type": "collective.rcse.group",
                 "sort_on": "sortable_title",
                 "sort_limit": 5,
                 "group_watchers": memberid}
        self.watched = catalog(**query)
