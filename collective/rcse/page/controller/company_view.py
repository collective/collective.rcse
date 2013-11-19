from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


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
