from AccessControl.SecurityManagement import newSecurityManager,\
    getSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from zope.component.hooks import getSite

from collective.whathappened.storage_manager import StorageManager
from collective.whathappened.notification import Notification


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
