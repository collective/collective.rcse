from zope import component
from zope import interface
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.rcse.content import member


class AuthenticatedMemberInfoView(BrowserView):
    """Person view helper to display member info"""
    interface.implements(member.IMember)
    member_schema = member.IMember

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
        self.fullname = None
        self.url = None
        self.dialog_url = None
        self.photo = None
        self.company = None
        self.function = None
        self.professional_email = None
        self.professional_mobile_phone = None

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

        attributes = list(self.member_schema.names())
        attributes += ['fullname']

        for attr in attributes:
            if getattr(self, attr, None) is None:
                value = self.member.getProperty(attr)
                if type(value) == object:
                    value = None
                setattr(self, attr, value)

class CreatorMemberInfoView(AuthenticatedMemberInfoView):
    """creator_memberinfo"""
    def update_member(self):
        if self.memberid is None:
            self.memberid = self.context.Creator()
        if self.member is None and self.memberid is not None:
            self.member = self.membership.getMemberById(self.memberid)


class MemberInfoView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_url = None
        self.membership = None
        self.wtool = None

    def __call__(self):
        self.update()
        self.getMemberProperties()
        if self.__name__.endswith("_view"):
            return self.index()
        return self

    def update(self):
        if self.portal_url is None:
            self.portal_url = getToolByName(self.context, 'portal_url')
        if self.membership is None:
            self.membership = getToolByName(self.context, "portal_membership")
        if self.wtool is None:
            self.wtool = getToolByName(self.context, 'portal_workflow')

    def getMemberProperties(self):
        self.member = self.membership.getMemberById(self.context.username)

        self.memberid = self.member.getProperty('username')
        self.url = '/'.join(self.context.getPhysicalPath())
        self.fullname = '%s %s' % (self.member.getProperty('first_name'),
                                   self.member.getProperty('last_name'))
        self.company = self.member.getProperty('company')
        self.function = self.member.getProperty('function')
        self.professional_email = self.member.getProperty('professional_email')
        self.professional_mobile_phone =\
            self.member.getProperty('professional_mobile_phone')
        self.state = self.getUserState()

    def getUserState(self):
        status = self.wtool.getStatusOf('collective_rcse_member_workflow',
                                        self.context)
        return status['review_state']
