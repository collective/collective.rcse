from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from AccessControl.unauthorized import Unauthorized
from collective.rcse.i18n import _

msg_unauthorized = _(u"You must be logged in to access to the RCSE")


class WelcomeView(BrowserView):
    """This is the page as default home when rcse is activated"""

    def __call__(self):
        self.update()
        if self.isAnon:
            raise Unauthorized(msg_unauthorized)
        return self.index()

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
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
