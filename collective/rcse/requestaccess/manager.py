from AccessControl.SecurityManagement import newSecurityManager,\
    getSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from plone.dexterity.utils import (
    createContent,
    addContentToContainer,
)
from plone.uuid.interfaces import IUUID, IUUIDAware
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.statusmessages.interfaces import IStatusMessage
from zope import component
from zope import event
from zope import interface
from plone.registry.interfaces import IRegistry

from collective.requestaccess import interfaces
from collective.requestaccess.i18n import _
from collective.rcse.requestaccess.interfaces import RequestSchema
from collective.rcse.requestaccess.event import RequestAddedEvent
from collective.rcse.requestaccess.event import RequestValidatedEvent
from collective.rcse.requestaccess.event import RequestRefusedEvent

import logging
from plone.app.uuid.utils import uuidToObject
logger = logging.getLogger("collective.requestaccess")


class ProxyRequest(object):
    interface.implements(RequestSchema)

    def __init__(self):
        self.id = None
        self.role = None
        self.target = None
        self.target_path = None
        self.target_title = ""
        self.rtype = "request"  # or "invitation"
        self.userid = None
        self.creatorid = None


class RequestManager(BrowserView):
    """implement the request manager as a view on plone site"""
    interface.implements(interfaces.IRequestManager)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.catalog = None
        self.container = None
        self.pstate = None
        self.memberid = None
        self.tools = None

    def __call__(self):
        self.update()
        return self  # make it useable inside template

    def update(self):
        if self.tools is None:
            self.tools = component.getMultiAdapter(
                (self.context, self.request),
                name="plone_tools"
            )
        if self.catalog is None:
            catalogid = 'portal_requestaccess_catalog'
            self.catalog = getToolByName(self.context, catalogid)
        if self.memberid is None:
            mtool = self.tools.membership()
            member = mtool.getAuthenticatedMember()
            if member is not None:
                self.memberid = member.getId()
        if self.pstate is None:
            self.pstate = component.getMultiAdapter(
                (self.context, self.request),
                name="plone_portal_state"
            )
        if self.container is None:
            portal = self.pstate.portal()
            self.container = portal.portal_requestaccess

    def create(self):
        self.update()
        proxy = ProxyRequest()
        proxy.userid = self.memberid
        proxy.creatorid = self.memberid
        proxy.target = str(IUUID(self.context))
        proxy.target_path = self.context.getPhysicalPath()
        proxy.target_title = self.context.Title()
        return proxy

    def _new_request(self):
        request = createContent(
            "collective.requestaccess",
        )
        return request

    def add(self, proxy):
        self.update()
        #TODO: check the role is at leat accessible to the current user
        userid = proxy.userid
        role = proxy.role
        target = proxy.target
        rid = self.normalize("r-%s-%s" % (userid, target))
        if rid in self.container.objectIds():
            return False
        request = self._new_request()
        request.id = rid
        request.role = role
        request.target = target
        request.target_path = proxy.target_path
        request.target_title = proxy.target_title
        request.userid = userid
        request.creatorid = proxy.creatorid
        request.rtype = proxy.rtype
        request.manage_setLocalRoles(userid, ["Owner"])
        #Give Owner role also to people who can validate the request
        local_roles = self.context.get_local_roles()
        for target_userid, roles in local_roles:
            if target_userid == userid:
                continue
            request.manage_setLocalRoles(target_userid, list(roles))
        addContentToContainer(self.container, request, checkConstraints=False)
        self.catalog.indexObject(self.container[rid])
        event.notify(RequestAddedEvent(self.container[rid]))
        return True

    def get(self, query=None):
        self.update()
        if query is None:
            query = {}
        brains = self.catalog(**query)
        requests = self._get_proxy_from_brain(brains)
        return requests

    def _get_proxy_from_brain(self, brains):
        proxies = []
        for brain in brains:
            request = brain.getObject()
            proxy = ProxyRequest()
            proxy.id = request.getId()
            proxy.role = request.role
            proxy.target = request.target
            proxy.target_path = request.target_path
            proxy.target_title = request.target_title
            proxy.rtype = request.rtype
            proxy.userid = request.userid
            proxy.creatorid = request.creatorid
            proxies.append(proxy)
        return proxies

    def remove(self, requestid):
        self.update()
        self.catalog.unindexObject(self.container[requestid])
        self.container._delObject(requestid)

    def get_current_id(self):
        self.update()
        if IUUIDAware.providedBy(self.context):
            target = str(IUUID(self.context))
        else:
            return None
        rid = self.normalize("r-%s-%s" % (self.memberid, target))
        return rid

    def get_current(self):
        """return None if no request on the current context"""
        self.update()
        current_id = self.get_current_id()
        if current_id is None:
            return
        request = getattr(self.container, current_id, None)
        if request is not None and request.rtype != "request":
            return
        return request

    def can_request(self, checkCurrent=True):
        """this method return True if the current authenticated
        member can make a request on the current context"""
        registry = component.getUtility(IRegistry)
        ptype = self.context.portal_type
        #white list check
        key_whitelist = "collective.request.access.filter.types_whitelist"
        whitelist = registry.get(key_whitelist, None)
        if whitelist is not None and ptype not in whitelist:
            return False

        #black list check
        key_blacklist = "collective.request.access.filter.types_blacklist"
        blacklist = registry.get(key_blacklist, None)
        if blacklist is not None and ptype in blacklist:
            return False

        if checkCurrent:
            #check existing request
            current_id = self.get_current_id()
            if current_id is None:
                return False
            exists = current_id in self.container.objectIds()
            return not exists

        return True

    def can_invite(self):
        """see iface"""
        return self.can_request(checkCurrent=False)

    def can_review(self):
        """see iface"""
        self.update()
        hasPerm = _checkPermission(
            "collective.requestaccess: Review request",
            self.context
        )
        hasRequests = False
        if hasPerm:
            query = {"target_path": '/'.join(self.context.getPhysicalPath())}
            hasRequests = bool(len(self.catalog(**query)))
        return hasPerm and hasRequests

    def normalize(self, oid):
        normalize = component.getUtility(IIDNormalizer).normalize
        return normalize(oid, max_length=80)

    def validate(self, rid):
        """Validate the request and add localrole.

        Security: A user can not validate a request for himself
        """
        self.update()
        request = self.container[rid]

        if request.creatorid == self.memberid:
            msg = _(u"You can 't validate your own request")
            IStatusMessage(self.request).add(msg)
            return

        self._validate_sudo(request)
        #delete the request
        event.notify(RequestValidatedEvent(self.container[rid]))
        self.remove(rid)

    def _validate_sudo(self, request):
        sm = getSecurityManager()
        acl_users = getToolByName(self.context, 'acl_users')
        tmp_user = UnrestrictedUser(
            sm.getUser().getId(), '', ['Manager'], ''
        )
        tmp_user = tmp_user.__of__(acl_users)
        newSecurityManager(None, tmp_user)
        role = request.role
        target = uuidToObject(request.target)
        target.manage_setLocalRoles(
            request.userid,
            [role]
        )
        target.reindexObject()
        setSecurityManager(sm)

    def refuse(self, rid):
        self.update()
        event.notify(RequestRefusedEvent(self.container[rid]))
        self.remove(rid)
