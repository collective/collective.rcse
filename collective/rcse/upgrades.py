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


def addTimeLineViewToContentTypes(context):
    common(context)
    ptypes = getToolByName(context, "portal_types")
    RCSE_CONTENT_TYPES = (
        'Document',
        'File',
        'Image',
        'News Item',
    )
    for t in RCSE_CONTENT_TYPES:
        fti = ptypes.getTypeInfo(t)
        if fti.default_view != "timeline_view":
            fti._updateProperty('default_view', "timeline_view")
        views = list(fti.view_methods)
        if "timeline_view" not in views:
            views.append("timeline_view")
            fti._updateProperty('view_methods', views)
