from AccessControl import getSecurityManager
from zope import component
from zope import interface
from zope import schema
from Products.Five.browser import BrowserView
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

from collective.rcse.content import member
from collective.rcse.i18n import _
from collective.rcse.content.visibility import NAMESPACE


class IMemberInfoView(interface.Interface):
    """ """
    def get_membrain():
        """Get membrane brain"""

    def get_membrane():
        """Get membrane object."""

    def get_settings():
        """Get user settings."""

class AuthenticatedMemberInfoView(BrowserView):
    """Person view helper to display member info"""
    interface.implements(member.IMember)
    member_schema = member.IMember
    member_fields = schema.getFieldNames(member.IMember)

    def __call__(self):
        self.update()
        if self.__name__.endswith("_view"):
            return self.index()
        return self

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        #dependencies
        self.portal_url = None
        self.membrane_tool = None
        self.membership = None
        self.memberid = None
        self.member = None
        self.url = None
        self.fullname = None

    @memoize
    def get_membrain(self):
        """return the member as a brain (Products.Membrane)"""
        brains = self.membrane_tool(exact_getUserId=self.memberid)
        if len(brains) == 1:
            return brains[0]

    @memoize
    def get_membrane(self):
        brain = self.get_membrain()
        if brain:
            return brain.getObject()

    @memoize
    def get_settings(self):
        membrane = self.get_membrane()
        return membrane.restrictedTraverse('get_settings')

    def update(self):
        self.update_dependencies()
        self.update_member()
        self.update_memberinfo()

    def update_dependencies(self):
        if self.portal_url is None:
            self.portal_url = getToolByName(self.context, "portal_url")
        if self.membership is None:
            self.membership = getToolByName(self.context, "portal_membership")
        if self.membrane_tool is None:
            self.membrane_tool = getToolByName(self.context, 'membrane_tool')

    def update_member(self):
        if self.member is None:
            self.member = self.membership.getAuthenticatedMember()
        if self.memberid is None:
            self.memberid = self.member.getId()

    def update_memberinfo(self):
        if self.memberid is None:
            raise ValueError("memberid can't be none")
        if self.url is None:
            self.url = self.portal_url() + '/author/' + self.memberid
        if self.fullname is None and self.member:
            self.fullname = self.member.getProperty('fullname')

    def __getattribute__(self, name):
        if name in AuthenticatedMemberInfoView.member_fields:
            membrane = self.get_membrane()
            if membrane is None:
                return None
            pref = '%s%s' % (NAMESPACE, name)
            if getattr(membrane, pref, True):
                return getattr(membrane, name)
            else:
                return ""
        else:
            return BrowserView.__getattribute__(self, name)

    def photo(self):
        membrane = self.get_membrane()
        if membrane:
            avatar = membrane.avatar
            if avatar:
                return "%s/@@images/avatar" % membrane.absolute_url()

        #TODO: replace by gravatar
        path = '/defaultUser.png/@@images/image'
        return self.portal_url() + path

    def emailIsValidated(self):
        return self.get_membrane().email_validation == 'ok'


class CreatorMemberInfoView(AuthenticatedMemberInfoView):
    """creator_memberinfo"""
    def update_member(self):
        if self.memberid is None:
            self.memberid = self.context.Creator()
        if self.member is None and self.memberid is not None:
            self.member = self.membership.getMemberById(self.memberid)
        if self.fullname is None:
            if self.member:
                self.fullname = self.member.getProperty('fullname')
            else:
                self.fullname = self.memberid


class BrainCreatorMemberInfoView(AuthenticatedMemberInfoView):
    """creator_memberinfo"""
    def update_member(self):
        if self.memberid is None:
            self.memberid = self.context.Creator
        if self.member is None and self.memberid is not None:
            self.member = self.membership.getMemberById(self.memberid)
        if self.fullname is None:
            if self.member:
                self.fullname = self.member.getProperty('fullname')
            else:
                self.fullname = self.memberid


class RequestMemberInfoView(AuthenticatedMemberInfoView):
    """member info throw request param
    """
    def update_member(self):
        if self.memberid is None:
            self.memberid = self.request.get("memberid", None)
        if self.member is None and self.memberid is not None:
            self.member = self.membership.getMemberById(self.memberid)


class GetMemberInfoView(AuthenticatedMemberInfoView):
    """Need to be called with userid parameter
    """
    def __call__(self, userid=None):
        if userid is None:
            return self
        self.memberid = userid
        self.update()

    def update_member(self):
        if self.member is None:
            self.member = self.membership.getMemberById(self.memberid)


class MemberInfoView(AuthenticatedMemberInfoView):

    def update_member(self):
        if self.member is None:
            self.member = self.membership.getMemberById(self.context.username)
        if self.memberid is None:
            self.memberid = self.member.getProperty('username')
        self.wftool = getToolByName(self.context, 'portal_workflow')
        status = self.wftool.getStatusOf(
            'collective_rcse_member_workflow',
            self.context
        )
        self.state = status.get('review_state', None)


# 
#         self.url = self.context.absolute_url()
#         self.fullname = '%s %s' % (self.member.getProperty('first_name'),
#                                    self.member.getProperty('last_name'))
#         self.company = self.member.getProperty('company')
#         self.function = self.member.getProperty('function')
#         self.professional_email = self.member.getProperty('professional_email')
#         self.professional_mobile_phone =\
#             self.member.getProperty('professional_mobile_phone')

    def getWorkflowTransitions(self):
        checkPermission = self.membership.checkPermission
        if not checkPermission(ReviewPortalContent, self.context):
            return None
        wtool = getToolByName(self.context, 'portal_workflow')
        transitions = wtool.getTransitionsFor(self.context)
        return transitions

    def getUserGroups(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(
            portal_type='collective.rcse.group',
            user_with_local_roles=self.memberid
            )
        return brains

    def canModify(self):
        checkPermission = self.membership.checkPermission
        if not checkPermission(ModifyPortalContent, self.context):
            return False
        return True
