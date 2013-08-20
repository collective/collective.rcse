from AccessControl.SecurityManagement import newSecurityManager,\
    getSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import getToolByName
from zope.component import getMultiAdapter


def createCompany(context, request):
    """"
    Context is user object.
    context.company is the company title.
    """
    portal_state = getMultiAdapter((context, request),
                                   name=u'plone_portal_state')
    directory = portal_state.portal()['companies_directory']
    sm = getSecurityManager()
    mtool = getToolByName(context, 'portal_membership')
    _sudo('Manager')
    company = createContentInContainer(
        directory,
        'collective.rcse.company',
        title=context.company
        )
    company.changeOwnership(mtool.getMemberById(context.username))
    company.manage_setLocalRoles(context.username, ['Owner'])
    company.setCreators([context.username])
    company.reindexObjectSecurity()
    setSecurityManager(sm)
    return company.id


def _sudo(self, role=None):
    """Give admin power to the current call"""
    if role is not None:
        sm = getSecurityManager()
        acl_users = getToolByName(self.context, 'acl_users')
        tmp_user = UnrestrictedUser(
            sm.getUser().getId(), '', [role], ''
            )
        tmp_user = tmp_user.__of__(acl_users)
        newSecurityManager(None, tmp_user)
