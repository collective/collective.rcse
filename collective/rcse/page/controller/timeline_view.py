from AccessControl.unauthorized import Unauthorized
from Products.CMFCore.utils import getToolByName

from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.page.controller.group_base import BaseView
from Products.Five.browser import BrowserView
from collective.rcse.content.group import get_group


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
        self.group = None

    def update(self):
        if self.plone_utils is None:
            self.plone_utils = getToolByName(self.context, 'plone_utils')
        if self.use_view_action is None:
            pp = getToolByName(self.context, 'portal_properties')
            self.use_view_action = pp.site_properties.getProperty(
                'typesUseViewActionInListings', ()
            )
        if self.group is None:
            self.group = get_group(self.context)
            self.group_title = self.group.Title()
            self.group_description = self.group.Description()
            self.group_url = self.group.absolute_url()
            self.group_photo = self.group.absolute_url() + "/group_photo"
            name = "@@plone.abovecontenttitle.documentactions"
            self.group_actions = self.group.restrictedTraverse(name)
        super(TimelineView, self).update()

    @property
    def filter_type(self):
        portal_types = self.plone_utils.getUserFriendlyTypes()
        portal_types.remove("collective.rcse.group")
        return portal_types


msg_unauthorized = _(u"You must be logged in to access to the RCSE")


class NavigationRootTimelineView(TimelineView):
    """This is the page as default home when rcse is activated"""

    def __call__(self):
        self.update()
        if self.isAnon:
            raise Unauthorized(msg_unauthorized)
        return self.index()

    def __init__(self, context, request):
        super(NavigationRootTimelineView, self).__init__(context, request)
        self.membership = None
        self.isAnon = None
        self.member = None

    def update(self):
        if self.group is None:
            self.group = self.context.restrictedTraverse('@@auth_memberinfo')
            self.group.update()
            self.group_title = self.group.fullname
            self.group_description = self.group.bio
            self.group_url = self.group.url
            self.group_photo = self.group.photo()
            self.group_actions = None
            #FEATURE: it should be easy to add doc actions on member profile
            #name = "@@plone.abovecontenttitle.documentactions"
            #self.group_actions = self.membrane.restrictedTraverse(name)
        super(NavigationRootTimelineView, self).update()
        if self.membership is None:
            self.membership = getToolByName(self.context, 'portal_membership')
        if self.member is None:
            self.member = self.membership.getAuthenticatedMember()
            if self.member.getId() is None:
                self.isAnon = True
        #hack the  query
        self.query["path"] = self.context_path
        self.query["group_watchers"] = self.member.getId()


class ContentAsTimeLineView(BrowserView):
    """We don't want to provide dedicated view for each content type so
    here is a base view to use the timeline template to display it"""

    def get_content(self, batch=True, b_size=10, b_start=0, pagerange=7,
                    full=False):
        return [{"getURL": self.context.absolute_url}]
