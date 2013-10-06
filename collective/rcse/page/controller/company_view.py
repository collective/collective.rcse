from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.rcse.page.controller.timeline_view import TimelineView


class CompanyInfoView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_url = None
        self.wtool = None
        self.catalog = None

    def __call__(self):
        self.update()
        self.url = self.context.absolute_url()
        if self.__name__.endswith("_view"):
            return self.index()
        return self

    def update(self):
        if self.portal_url is None:
            self.portal_url = getToolByName(self.context, 'portal_url')
        if self.wtool is None:
            self.wtool = getToolByName(self.context, 'portal_workflow')
        if self.catalog is None:
            self.catalog = getToolByName(self.context, 'portal_catalog')


class CompanyTimelineView(BrowserView):
    is_content_timeline = True

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_url = getToolByName(self.context, 'portal_url')

        self.group = self.context
        self.group_title = self.context.Title()
        name = "@@company_description_view"
        self.group_description = self.context.restrictedTraverse(name)()
        self.group_url = self.group.absolute_url()
        if self.context.logo:
            self.group_photo = "%s/@@images/logo" % self.group_url
        else:
            self.group_photo = None
        self.group_actions = None
        name = "@@collective.rcse.editbar"
        self.group_edit_bar = self.context.restrictedTraverse(name)
        name = "@@plone.abovecontenttitle.documentactions"
        self.group_actions = self.group.restrictedTraverse(name)

    def get_content(self, **kwargs):
        return self.catalog(company_id=self.context.getId())
