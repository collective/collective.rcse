from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class VCardView(BrowserView):
    """VCard view helper to display member info"""

    def __call__(self):
        self.update()
        return self.index()

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.portal_url = None
        self.membership = None
        self.memberid = None
        self.member = None

        self.fn = None
        self.nickname = None
        self.photo = None
        self.title = None
        self.role = None
        self.url = None
        self.org = None
        self.addr = None

    def update(self):
        if self.portal_url is None:
            self.portal_url = getToolByName(self.context, "portal_url")
        if self.membership is None:
            self.membership = getToolByName(self.context, "portal_membership")
        if self.memberid is None:
            self.memberid = self.request.get("vcardmemberid", None)
        if self.memberid is None:
            self.memberid = self.context.Creator()
        if self.member is None and self.memberid is not None:
            self.member = self.membership.getMemberById(self.memberid)

        if self.fn is None:
            self.fn = self.request.get("vcardfn", None)
        if self.fn is None:
            self.fn = self.member.getProperty('fullname')
        if self.url is None:
            self.url = self.request.get("vcardurl", None)
        if self.url is None:
            self.url = self.portal_url + '/author/' + self.memberid
        if self.photo is None:
            self.photo = self.request.get("vcardphoto", None)
        if self.photo is None:
            photo = self.membership.getPersonalPortrait(self.memberid)
            if photo:
                self.photo = photo.absolute_url()
            else:
                path = '/++resource++collective.rcse/defaultUser.png'
                self.photo = self.portal_url() + path
