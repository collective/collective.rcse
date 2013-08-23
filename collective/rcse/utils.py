from AccessControl.SecurityManagement import newSecurityManager,\
    getSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from zope.component.hooks import getSite


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
