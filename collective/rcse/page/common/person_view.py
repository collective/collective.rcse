from zope import interface
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.rcse.content import member


class AuthenticatedMemberInfoView(BrowserView):
    """Person view helper to display member info"""
    interface.implements(member.IMember)

    def __call__(self):
        self.update()
        if self.__name__.endswith("_view"):
            return self.index()
        return self

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        #dependencies
        self.portal_url = None
        self.membership = None
        self.memberid = None
        self.member = None

        #info
        self.url = None
        self.photo = None

    def update(self):
        self.update_dependencies()
        self.update_member()
        self.update_memberinfo()

    def update_dependencies(self):
        if self.portal_url is None:
            self.portal_url = getToolByName(self.context, "portal_url")
        if self.membership is None:
            self.membership = getToolByName(self.context, "portal_membership")

    def update_member(self):
        if self.member is None:
            self.member = self.membership.getAuthenticatedMember()
        if self.memberid is None:
            self.memberid = self.member.getId()

    def update_memberinfo(self):
        if self.member is None:
            raise ValueError("member can t be none")
        if self.url is None:
            self.url = self.portal_url() + '/author/' + self.memberid
        if self.photo is None:
            photo = self.membership.getPersonalPortrait(self.memberid)
            if photo:
                self.photo = photo.absolute_url()
            else:
                #TODO: replace by gravatar
                path = '/++resource++collective.rcse/defaultUser.png'
                self.photo = self.portal_url() + path
        # @TODO Load attributes from member schema
        attributes = ('fullname',)
        for attr in attributes:
            if getattr(self, attr, None) is None:
                setattr(self, attr, self.member.getProperty(attr))

class CreatorMemberInfoView(AuthenticatedMemberInfoView):
    def update_member(self):
        if self.memberid is None:
            self.memberid = self.context.Creator()
        if self.member is None and self.memberid is not None:
            self.member = self.membership.getMemberById(self.memberid)
