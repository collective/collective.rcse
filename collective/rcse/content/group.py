from Products.Five.browser import BrowserView
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class GroupView(BrowserView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        pass
