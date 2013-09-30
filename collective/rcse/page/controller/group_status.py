from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class GroupStatusView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.portal_workflow = getToolByName(self.context, 'portal_workflow')
        self.review_state = self.portal_workflow.getInfoFor(
            self.context, "review_state"
        )

    def is_private(self):
        return self.review_state == "private"

    def is_open(self):
        return self.review_state == "open"

    def is_moderated(self):
        return self.review_state == "moderated"
