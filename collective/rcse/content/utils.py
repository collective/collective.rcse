from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import getToolByName
from zope.component import getMultiAdapter
from zope.i18n import translate

from collective.rcse.utils import sudo
from collective.rcse.i18n import _

@sudo()
def createCompany(context, request, username=None, company_name=None):
    if username is None:
        username = context.username
    if company_name is None:
        company_name = context.company
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
#    _createCompaniesGroups(home, company, username,
#                           mtool, auth_user, request)
    return company.id


def _createCompaniesGroups(home, company, username,
                           mtool, auth_user, request):
    private_group = createContentInContainer(
        home,
        'collective.rcse.group',
        title=translate(_(u"${company}'s private group",
                          mapping={'company': company.title}),
                        context=request
                        )
    )
    private_group.manage_delLocalRoles([auth_user])
    private_group.changeOwnership(mtool.getMemberById(username))
    private_group.manage_setLocalRoles(username, ['Owner'])
    private_group.setCreators([username])
    private_group.reindexObjectSecurity()
    company.private_group = private_group.id
    public_group = createContentInContainer(
        home,
        'collective.rcse.group',
        title=translate(_(u"${company}'s public group",
                          mapping={'company': company.title}),
                        context=request
                        )
    )
    public_group.manage_delLocalRoles([auth_user])
    public_group.changeOwnership(mtool.getMemberById(username))
    public_group.manage_setLocalRoles(username, ['Owner'])
    public_group.setCreators([username])
    public_group.reindexObjectSecurity()
    wtool = getToolByName(company, 'portal_workflow')
    wtool.doActionFor(public_group, 'show_internally')
    company.public_group = public_group.id
