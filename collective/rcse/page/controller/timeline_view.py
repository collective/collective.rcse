from collective.rcse.page.controller import group_timeline_view
from AccessControl.unauthorized import Unauthorized
from collective.rcse.i18n import RCSEMessageFactory
from plone.uuid.interfaces import IUUID
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

_ = RCSEMessageFactory

GroupTimelineView = group_timeline_view.TimelineView
msg_unauthorized = _(u"You must be logged in to access to the RCSE")


class TimelineView(GroupTimelineView):
    """This is the page as default home when rcse is activated"""

    def __call__(self):
        self.update()
        if self.isAnon:
            raise Unauthorized(msg_unauthorized)
        return self.index()

    def __init__(self, context, request):
        super(TimelineView, self).__init__(context, request)
        self.membership = None
        self.isAnon = None
        self.member = None

    def update(self):
        super(TimelineView, self).update()
        if self.membership is None:
            self.membership = getToolByName(self.context, 'portal_membership')
        if self.member is None:
            self.member = self.membership.getAuthenticatedMember()
            if self.member.getId() is None:
                self.isAnon = True
        #hack the  query
        self.query["path"] = self.context_path
        self.query["group_watchers"] = self.member.getId()
