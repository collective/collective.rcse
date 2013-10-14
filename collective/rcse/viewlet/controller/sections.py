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
        memberid = self.portal_state.member().getId()
        favmanager = self.context.restrictedTraverse(VIEW_NAME)
        catalog = getToolByName(self.context, 'portal_catalog')

        query = {"portal_type": "collective.rcse.group",
                 "sort_on": "sortable_title",
                 "sort_limit": 5}
        self.favorites = [f for f in favmanager.get(query=query)
                          if f.Creator != memberid]
#        query = {"portal_type": "collective.rcse.group",
#                 "sort_on": "sortable_title",
#                 "sort_limit": 5,
#                 "group_watchers": memberid}
#        self.watched = catalog(**query)

        query = {"portal_type": "collective.rcse.group",
                 "sort_on": "sortable_title",
                 "user_with_local_roles": memberid}
        self.registred = [r for r in catalog(**query)
                          if r.Creator != memberid]

        query = {"portal_type": "collective.rcse.group",
                 "sort_on": "sortable_title",
                 "Creator": memberid}
        self.my_groups = catalog(**query)
