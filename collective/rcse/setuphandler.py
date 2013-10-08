## setuphandlers.py
import logging
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.contentrules.rule import Rule, get_assignments
from plone.app.controlpanel.security import ISecuritySchema
from plone.contentrules.engine.assignments import RuleAssignment
from plone.contentrules.engine.interfaces import IRuleStorage,\
    IRuleAssignmentManager
from plone.contentrules.rule.interfaces import IRuleAction, IRuleCondition
from zope.globalrequest import getRequest
from zope import component

from cioppino.twothumbs.event import ILikeEvent
from collective.rcse.i18n import _
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.interface.declarations import alsoProvides
from Products.membrane.config import TOOLNAME
from zExceptions import BadRequest

LOG = logging.getLogger("collective.history")


def setupVarious(context):
    """Create the history container"""

    if context.readDataFile('collective_rcse.txt') is None:
        return

    portal = context.getSite()
    installOnce(portal)
    updateWelcomePage(portal)
    createDirectories(portal)
    setupRegistration(portal)
    initialize_rules(portal)
    setupCatalog(portal)
    fixMembraneCatalog(portal)
    uninstallDependencies(portal)
    activateComments(portal)
    deactivateSourceUsers(portal)
    addTimelineViewToContentTypes(portal)
    renameDocumentToArticle(portal)


def deactivateSourceUsers(portal):
    acl_users = getToolByName(portal, 'acl_users')
    source_users = acl_users['source_users']
    source_users.manage_activateInterfaces([])


def setupRegistration(site):
    securitySchema = ISecuritySchema(site)
    securitySchema.enable_self_reg = True
    securitySchema.enable_user_pwd_choice = True


def setupCatalog(portal):
    catalog = getToolByName(portal, 'portal_catalog')
    if 'group_watchers' not in catalog.Indexes:
        catalog.addIndex('group_watchers', 'KeywordIndex')
    if 'username' in catalog.Indexes:
        catalog.delIndex('username')
    if 'company_id' not in catalog.Indexes:
        catalog.addIndex('company_id', 'FieldIndex')
    if 'user_with_local_roles' not in catalog.Indexes:
        catalog.addIndex('user_with_local_roles', 'KeywordIndex')


def createDirectories(parent):
    existing = parent.objectIds()
    if "users_directory" not in existing:
        _createObjectByType(
            "collective.rcse.directory",
            parent,
            id="users_directory",
            title=_(u"Users directory")
        )
    _updateFolder(
        parent.users_directory,
        ['collective.rcse.member'],
        "users_directory_view"
        )
    _publishContent(parent.users_directory)
    if "companies_directory" not in existing:
        _createObjectByType(
            "collective.rcse.directory",
            parent,
            id="companies_directory",
            title=_(u"Companies directory")
        )
    _updateFolder(
        parent.companies_directory,
        ['collective.rcse.company'],
        "companies_directory_view",
        )
    _publishContent(parent.companies_directory)
    if "home" not in existing:
        _createObjectByType(
            "Folder",
            parent,
            id="home",
            title=_(u"Home")
        )
    _updateFolder(
        parent.home,
        ['collective.rcse.group'],
        "timeline_view",
        )
    alsoProvides(parent.home, INavigationRoot)
    _publishContent(parent.home)
    parent.home.reindexObject()


def _publishContent(content):
    wtool = getToolByName(content, 'portal_workflow')
    try:
        wtool.doActionFor(content, 'publish_internally')
    except WorkflowException:
        pass  # Content has already been published


def _updateFolder(obj, types=None, view=None, authenticated_roles=None):
    if view is not None:
        obj.setLayout(view)
    if types is not None:
        aspect = ISelectableConstrainTypes(obj)
        addable = aspect.getLocallyAllowedTypes()
        if types != addable:
            aspect.setConstrainTypesMode(1)
            # Need to be globally allowed in order to be set as locally allowed
            #     or to create a custom folderish content type with
            #     "allowed_content_types"
            # Only a blacklist, not a whitelist
            setattr(obj, 'locally_allowed_types', types)
            setattr(obj, 'immediately_addable_types', types)
    if authenticated_roles is not None:
        obj.manage_setLocalRoles('AuthenticatedUsers', authenticated_roles)


def updateWelcomePage(site):
    layout = site.getLayout()
    if layout != "rcse_redirect_view":
        site.setLayout("rcse_redirect_view")


def initialize_rules(portal):
    storage = component.getUtility(IRuleStorage)
    request = getRequest()
    if 'subscribe_on_like' not in storage:
        _subscribe_on_like_rule(portal, request)
    if 'watch_on_like' not in storage:
        _watch_on_like_rule(portal, request)


def _subscribe_on_like_rule(portal, request):
    RULE_ID = 'subscribe_on_like'
    rule = _create_rule(portal,
                        RULE_ID,
                        "Subscribe on like",
                        ILikeEvent)
    #add condition & action
    data = {'check_types': ['collective.rcse.group']}
    _add_rule_condition(
        request,
        rule,
        'plone.conditions.PortalType',
        data
        )
    data = {'preference': 'subscribe_when_favorited', 'condition': True}
    _add_rule_condition(
        request,
        rule,
        'collective.rcse.conditions.Preference',
        data
        )

    data = {'subscription': 'subscribe'}
    action = 'collective.whathappened.actions.Subscription'
    _add_rule_action(request, rule, action, data)
    #activate it on context
    _activate_rule(RULE_ID, portal)


def _watch_on_like_rule(portal, request):
    RULE_ID = 'watch_on_like'
    rule = _create_rule(portal,
                        RULE_ID,
                        "Watch on like",
                        ILikeEvent)

    data = {'preference': 'watch_when_favorited', 'condition': True}
    _add_rule_condition(
        request,
        rule,
        'collective.rcse.conditions.Preference',
        data
        )

    data = {'watching': 'watch'}
    action = 'collective.watcherlist.actions.Watching'
    _add_rule_action(request, rule, action, data)
    #activate it on context
    _activate_rule(RULE_ID, portal)


def _add_rule_condition(request, rule, condition_id, data):
    condition = component.getUtility(IRuleCondition, name=condition_id)
    adding = rule.restrictedTraverse('+condition')
    addview = adding.restrictedTraverse(str(condition.addview))
    #adding = component.getMultiAdapter((rule, request), name='+condition')
#    addview = component.getMultiAdapter((adding, request),
#                                        name=condition.addview)
    addview.createAndAdd(data=data)


def _add_rule_action(request, rule, action_id, data):
    action = component.getUtility(IRuleAction, name=action_id)
    adding = rule.restrictedTraverse('+action')
    addview = adding.restrictedTraverse(str(action.addview))
#    adding = component.getMultiAdapter((rule, request), name='+action')
#    addview = component.getMultiAdapter((adding, request), name=action.addview)
    addview.createAndAdd(data=data)


def _create_rule(portal, rule_id, title, event):
    storage = component.getUtility(IRuleStorage)
    if rule_id not in storage:
        storage[rule_id] = Rule()
    rule = storage.get(rule_id)
    rule.title = title
    rule.enabled = True
    # Clear out conditions and actions since we're expecting new ones
    del rule.conditions[:]
    del rule.actions[:]
    rule.event = event
    rule = rule.__of__(portal)
    return rule


def _activate_rule(rule_id, context=None):
    storage = component.getUtility(IRuleStorage)
    rule = storage.get(rule_id)
    assignable = IRuleAssignmentManager(context)
    assignment = assignable.get(rule_id, None)
    if not assignment:
        assignment = assignable[rule_id] = RuleAssignment(rule_id)
    assignment.enabled = True
    assignment.bubbles = True
    get_assignments(rule).insert('/'.join(context.getPhysicalPath()))


def fixMembraneCatalog(context):
    """don't know why but each time we apply the profile the membrane
    catalog is empty."""
    catalog = getToolByName(context, TOOLNAME, None)
    catalog.refreshCatalog(clear=1)


def uninstallDependencies(context):
    UNINSTALL = ("collective.z3cform.widgets",)
    qi = getToolByName(context, 'portal_quickinstaller')
    qi.uninstallProducts(UNINSTALL)
    #TODO: unstinstall this please ...


def activateComments(portal):
    """This activate comments on all content types"""
    property = 'allow_discussion'
    portal_types = getToolByName(portal, 'portal_types')
    for portal_type in portal_types.listContentTypes():
        document_fti = getattr(portal_types, portal_type)
        try:
            document_fti._updateProperty(property, True)
        except BadRequest:
            continue


def addTimelineViewToContentTypes(context):
    ptypes = getToolByName(context, "portal_types")
    RCSE_CONTENT_TYPES = (
        'Document',
        'File',
        'Image',
        'News Item',
        'collective.polls.poll',
    )
    for t in RCSE_CONTENT_TYPES:
        fti = ptypes.getTypeInfo(t)
        if fti.default_view != "timeline_view":
            fti._updateProperty('default_view', "timeline_view")
        views = list(fti.view_methods)
        if "timeline_view" not in views:
            views.append("timeline_view")
            fti._updateProperty('view_methods', views)


def renameDocumentToArticle(context):
    """plone.po doesn't work... so let's just rename the title of the type"""
    ptypes = getToolByName(context, "portal_types")
    fti = ptypes.getTypeInfo("Document")
    fti._updateProperty('title', "Article")


def installOnce(context):
    """Some addon like Products.mebrane must be installed once, the profile
    must not be re-applied because it use catalog.xml
    """
    #first install Products.mebrane if not already installed
    qi = getToolByName(context, "portal_quickinstaller")
    addons = ["Products.membrane",
              "cioppino.twothumbs",
              "collective.favoriting"]
    for addon in addons:
        if qi.isProductInstallable(addon):
            qi.installProduct(addon)
