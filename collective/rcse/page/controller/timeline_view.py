from AccessControl.unauthorized import Unauthorized
from Products.CMFCore.utils import getToolByName

from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.page.controller.group_base import BaseView
from Products.Five.browser import BrowserView
from collective.rcse.content.group import get_group
from Products.CMFCore import permissions
from collective.rcse.page.controller.poll_view import PollView


_ = RCSEMessageFactory
msg_unauthorized = _(u"You must be logged in to access to the RCSE")


class GroupTimelineView(BaseView):
    """Timeline view"""
    is_content_timeline = False
    label_content = _(u"News")
    label_timeline = _(u"Group")

    def __call__(self):
        self.update()
        return self.index()

    def __init__(self, context, request):
        super(GroupTimelineView, self).__init__(context, request)
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
            name = "@@timeline_header_group"
            self.group_description = self.group.restrictedTraverse(name)()
        super(GroupTimelineView, self).update()

    @property
    def filter_type(self):
        portal_types = self.plone_utils.getUserFriendlyTypes()
        #portal_types.remove("collective.rcse.group")
        return portal_types


class NavigationRootTimelineView(GroupTimelineView):
    """This is the page as default home when rcse is activated"""
    label_content = _(u"News")
    label_timeline = _(u"My profile")

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
        if self.membership is None:
            self.membership = getToolByName(self.context, 'portal_membership')
        if self.member is None:
            self.member = self.membership.getAuthenticatedMember()
            if self.member.getId() is None:
                self.isAnon = True
        if self.isAnon:
            self.group = self.member
        if self.group is None:
            self.group = True
            name = "@@timeline_header_navroot_view"
            self.group_description = self.context.restrictedTraverse(name)()
        super(NavigationRootTimelineView, self).update()

        self.query["path"] = self.context_path
        self.query["group_watchers"] = self.member.getId()


class ContentAsTimelineView(BrowserView):
    """We don't want to provide dedicated view for each content type so
    here is a base view to use the timeline template to display it"""
    is_content_timeline = True
    label_content = None

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.group = None

    def get_content(self, **kwargs):
        return [{"getURL": self.context.absolute_url}]


class ProxyGroupTimelineView(BrowserView):
    is_content_timeline = True
    label_content = _(u"Moderated group")

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.manager = self.context.restrictedTraverse("@@proxy_group_manager")
        self.manager.update()
        self.mtool = getToolByName(self.context, 'portal_membership')
        checkPermission = self.mtool.checkPermission
        if checkPermission(permissions.View, self.manager.group):
            self.request.response.redirect(self.manager.group.absolute_url())
        self.group = self.context
        self.group_title = self.manager.title()
        self.group_url = self.group.absolute_url()
        name = "@@timeline_header_group"
        self.group_description = self.context.restrictedTraverse(name)()

    def get_content(self, **kwargs):
        return []


class MemberTimelineView(GroupTimelineView):
    label_timeline = _(u"Member")
    def update(self):
        if self.group is None:
            self.group = self.context
            self.group_title = _(u"Member")
            description = self.context.restrictedTraverse('@@timeline_header_member_view')()
            self.group_description = description
        super(MemberTimelineView, self).update()
        self.query["Creator"] = self.context.username
        del self.query['path']
        self.label_content = _(
            u"Contents created by ${name}",
            mapping={'name': self.group.Title()}
        )
        wftool = getToolByName(self.context, 'portal_workflow')
        self.group_review_state = wftool.getInfoFor(
            self.context, "review_state", None
        )
        if self.group_review_state != "enabled":
            self.is_content_timeline = True

    def get_content(self, **kwargs):
        if self.group_review_state != "enabled":
            return []
        return super(MemberTimelineView, self).get_content()

class CompanyTimelineView(BrowserView):
    is_content_timeline = False
    label_content = _(u"Members")

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_url = getToolByName(self.context, 'portal_url')
        self.context_path = '/'.join(self.context.getPhysicalPath())

        self.group = self.context
        self.group_title = _(u"Company")  # the title is already in the desc
        self.group_url = self.group.absolute_url()
        name = "@@timeline_header_company"
        self.group_description = self.context.restrictedTraverse(name)()


    def get_content(self, **kwargs):
        return self.catalog(company_id=self.context.getId())


class PollTimelineView(ContentAsTimelineView, PollView):
    def __init__(self, context, request):
        ContentAsTimelineView.__init__(self, context, request)
        PollView.__init__(self, context, request)

    def update(self):
        ContentAsTimelineView.update(self)
        PollView.update(self)
