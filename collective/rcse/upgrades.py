from plone.contentrules.engine.interfaces import IRuleStorage
from Products.CMFCore.utils import getToolByName
from zope import component
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


def add_watcher_adapter_name_to_content_rule(context):
    common(context)
    storage = component.getUtility(IRuleStorage)
    action = storage['watch_on_like'].actions[0]
    if not hasattr(action, 'name') or not action.name:
        setattr(action, 'name', 'group_watchers')

