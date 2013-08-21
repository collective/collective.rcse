from AccessControl.SecurityManagement import newSecurityManager,\
    getSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import getToolByName
from zope.component import getMultiAdapter
from zope.i18n import translate

from collective.rcse.i18n import _


def createCompany(context, request):
    """"
    Context is user object.
    context.company is the company title.
    """
    portal_state = getMultiAdapter((context, request),
                                   name=u'plone_portal_state')
    directory = portal_state.portal()['companies_directory']
    home = portal_state.portal()['home']
    sm = getSecurityManager()
    mtool = getToolByName(context, 'portal_membership')
    auth_user = mtool.getAuthenticatedMember().getId()
    _sudo('Manager')
    company = createContentInContainer(
        directory,
        'collective.rcse.company',
        title=context.company
        )
    company.manage_delLocalRoles([auth_user])
    company.changeOwnership(mtool.getMemberById(context.username))
    company.manage_setLocalRoles(context.username, ['Owner'])
    company.setCreators([context.username])
    company.reindexObjectSecurity()
    _createCompaniesGroups(home, company, context.username,
                           mtool, auth_user, request)
    setSecurityManager(sm)
    return company.id


def _createCompaniesGroups(home, company, username,
                           mtool, auth_user, request):
    private_group = createContentInContainer(
        home,
        'collective.rcse.group',
        title=translate(u"${company}'s private group",
                        domain='collective.rcse',
                        mapping={'company': company.title},
                        context=request
                        )
        )
    private_group.manage_delLocalRoles([auth_user])
    private_group.changeOwnership(mtool.getMemberById(username))
    private_group.manage_setLocalRoles(username, ['Owner'])
    private_group.setCreators([username])
    private_group.reindexObjectSecurity()
    # TODO (Workflow) set group to private group
    company.private_group = private_group.id
    public_group = createContentInContainer(
        home,
        'collective.rcse.group',
        title=translate(u"${company}'s public group",
                        domain='collective.rcse',
                        mapping={'company': company.title},
                        context=request
                        )
        )
    public_group.manage_delLocalRoles([auth_user])
    public_group.changeOwnership(mtool.getMemberById(username))
    public_group.manage_setLocalRoles(username, ['Owner'])
    public_group.setCreators([username])
    public_group.reindexObjectSecurity()
    # TODO (Workflow) set group to public group
    company.public_group = public_group.id


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
