from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class WelcomeView(BrowserView):
    """This is the page as default home when rcse is activated"""

    def __call__(self):
        self.update()
        return self.index()

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.membership = None

    def update(self):
        if self.membership is None:
            self.membership = getToolByName(self.context, 'portal_membership')
