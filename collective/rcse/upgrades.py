from Products.CMFCore.utils import getToolByName
PROFILE = 'profile-collective.rcse:default'


def common(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE)


def make_group_owner_siteadmin(context):
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog(portal_type="collective.rcse.group")
    roles = ["Owner", "Site Administrator"]

    for brain in brains:
        group = brain.getObject()
        creators = group.creators
        for creator in creators:
            group.manage_setLocalRoles(creator, roles)

