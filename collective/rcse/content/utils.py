from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import getToolByName
from zope.component import getMultiAdapter
from zope.i18n import translate

from collective.rcse.i18n import _
from collective.rcse.utils import sudo


@sudo()
def createCompany(context, request, username, company_name):
    portal_state = getMultiAdapter((context, request),
                                   name=u'plone_portal_state')
    directory = portal_state.portal()['companies_directory']
    home = portal_state.portal()['home']
    mtool = getToolByName(context, 'portal_membership')
    auth_user = mtool.getAuthenticatedMember().getId()
    company = createContentInContainer(
        directory,
        'collective.rcse.company',
        title=company_name
        )
    company.manage_delLocalRoles([auth_user])
    company.changeOwnership(mtool.getMemberById(username))
    company.manage_setLocalRoles(username, ['Owner'])
    company.setCreators([username])
    company.reindexObjectSecurity()
    _createCompaniesGroups(home, company, username,
                           mtool, auth_user, request)
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
