from AccessControl.unauthorized import Unauthorized
from Products.CMFCore.utils import getToolByName

from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.page.controller.group_base import BaseView
from Products.Five.browser import BrowserView
from collective.rcse.content.group import get_group
from Products.CMFCore import permissions


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
#            self.group_title = self.group.Title()
#            self.group_description = self.group.Description()
#            self.group_url = self.group.absolute_url()
#            self.group_photo = self.group.absolute_url() + "/group_photo"
#            name = "@@plone.abovecontenttitle.documentactions"
#            self.group_actions = self.group.restrictedTraverse(name)
#            name = "@@collective.rcse.editbar"
#            self.group_edit_bar = self.group.restrictedTraverse(name)
        super(GroupTimelineView, self).update()

    @property
    def filter_type(self):
        portal_types = self.plone_utils.getUserFriendlyTypes()
        portal_types.remove("collective.rcse.group")
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
#            self.group = self.context.restrictedTraverse('@@auth_memberinfo')
#            self.group.update()
            name = "@@timeline_header_navroot_view"
            self.group_description = self.context.restrictedTraverse(name)()
#            membrane = self.group.get_membrane()
#            self.group_url = membrane.absolute_url()
#            self.group_title = self.group.fullname
#            description = membrane.restrictedTraverse('@@tile_view')()
#            self.group_description = description
#            self.group_photo = self.group.photo()
#            self.group_actions = None
#            self.group_edit_bar = None
        super(NavigationRootTimelineView, self).update()
        #hack the  query
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
    label_content = None

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        #TODO: check if current user as view access to the real group and redirect
        self.manager = self.context.restrictedTraverse("@@proxy_group_manager")
        self.manager.update()
        self.mtool = getToolByName(self.context, 'portal_membership')
        checkPermission = self.mtool.checkPermission
        if checkPermission(permissions.View, self.manager.group):
            self.request.response.redirect(self.manager.group.absolute_url())
        self.group = self.context
        self.group_title = self.manager.title()
        self.group_url = self.group.absolute_url()
#        self.group_description = self.manager.description()
#        self.group_photo = self.group_url + "/group_photo"
#        self.group_actions = None
#        name = "@@collective.rcse.editbar"
#        self.group_edit_bar = self.context.restrictedTraverse(name)

    def get_content(self, **kwargs):
        return []


class MemberTimelineView(GroupTimelineView):
    label_timeline = _(u"Member")
    def update(self):
        if self.group is None:
            self.group = self.context
            self.group_title = _(u"Member")
#            self.group_url = self.group.absolute_url()
            description = self.context.restrictedTraverse('@@timeline_header_member_view')()
            self.group_description = description
#            self.group_photo = None
#            name = "@@plone.abovecontenttitle.documentactions"
#            self.group_actions = self.group.restrictedTraverse(name)
#            name = "@@collective.rcse.editbar"
#            self.group_edit_bar = self.group.restrictedTraverse(name)
        super(MemberTimelineView, self).update()
        self.query["Creator"] = self.context.username
        del self.query['path']
        self.label_content = _(
            u"Contents created by ${name}",
            mapping={'name': self.group.Title()}
        )


class CompanyTimelineView(BrowserView):
    is_content_timeline = False
    label_content = _(u"Members")

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_url = getToolByName(self.context, 'portal_url')

        self.group = self.context
        self.group_title = _(u"Company")  # the title is already in the desc
        self.group_url = self.group.absolute_url()
        name = "@@timeline_header_company"
        self.group_description = self.context.restrictedTraverse(name)()
#        if self.context.logo:
#            self.group_photo = "%s/@@images/logo" % self.group_url
#        else:
#            self.group_photo = None
#        self.group_actions = None
#        name = "@@collective.rcse.editbar"
#        self.group_edit_bar = self.context.restrictedTraverse(name)
#        name = "@@plone.abovecontenttitle.documentactions"
#        self.group_actions = self.group.restrictedTraverse(name)

    def get_content(self, **kwargs):
        return self.catalog(company_id=self.context.getId())
