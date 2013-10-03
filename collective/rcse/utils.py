from AccessControl.SecurityManagement import newSecurityManager,\
    getSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from zope.component.hooks import getSite

from Products.CMFCore.utils import getToolByName

from collective.whathappened.storage_manager import StorageManager
from collective.whathappened.notification import Notification
from Products.Five.browser import BrowserView
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin,\
    IUserAdderPlugin, IUserEnumerationPlugin


def sudo(role='Manager'):
    """Give admin power to the current call"""

    def wrapper(fct):
        def wrapper(*args, **kwargs):
            sm = getSecurityManager()
            acl_users = getSite().acl_users
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', [role], ''
                )
            tmp_user = tmp_user.__of__(acl_users)
            newSecurityManager(None, tmp_user)
            ret = fct(*args, **kwargs)
            setSecurityManager(sm)
            return ret
        return wrapper
    return wrapper


def createNotification(what, where, when, who, user):
    """Create a new notification and store it."""

    storage = StorageManager(getSite())
    storage.setUser(user)
    notification = Notification(what, where, when, who, user, 'rcse_utils')
    storage.initialize()
    storage.storeNotification(notification)
    storage.terminate()


class DevSyncUsers(BrowserView):
    """Add users from cas to sources_users"""
    def __call__(self):
        self.acl_users = getToolByName(self.context, 'acl_users')
        self.source_users = self.acl_users['source_users']
        self.cas = self.acl_users['cas']
        self.membrane_tool = getToolByName(self.context, 'membrane_tool')
        self.sync()
        self.fix_not_indexed_users()

        dev = self.request.get('dev', False)
        if dev:
            self.activate_source_users()
            self.desactivate_cas()
            self.create_test_users()

    def sync(self):
        for brain in self.membrane_tool():
            try:
                member = brain.getObject()
            except:
                continue
            username = member.username
            find = False
            if self.source_users.enumerateUsers(id=username):
                #FIXME: update password
                continue
            #add it
            self.source_users.doAddUser(username, 'makina')

    def activate_source_users(self):
        self.source_users.manage_activateInterfaces([
            "IAuthenticationPlugin",
            "IUserAdderPlugin",
            "IUserEnumerationPlugin"
        ])

    def desactivate_cas(self):
        self.cas.manage_activateInterfaces([])

    def create_test_users(self):
        """create testuser1, testuser2"""
        TEST_USERS = [("testuser1", "makina"), ("testuser2", "makina")]
        regtool = getToolByName(self.context, 'portal_registration')
        for username, password in TEST_USERS:
            regtool.addMember(username, password)
            #TODO: add member role

    def fix_not_indexed_users(self):
        indexed = [brain.getObject() for brain in self.membrane_tool()]
        membranes = self.context.users_directory.contentItems()
        if len(membranes) > len(indexed):
            for mid, membrane in membranes:
                if membrane not in indexed:
                    self.membrane_tool.reindexObject(membrane)
