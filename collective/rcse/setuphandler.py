## setuphandlers.py
import logging
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.interfaces import IDexterityContainer

from collective.rcse.i18n import _

LOG = logging.getLogger("collective.history")


def setupVarious(context):
    """Create the history container"""

    if context.readDataFile('collective_rcse.txt') is None:
        return

    portal = context.getSite()
    updateWelcomePage(portal)
    createDirectories(portal)


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
        ['Contributor']
        )
    _publishContent(parent.companies_directory)


def _publishContent(content):
    wtool = getToolByName(content, 'portal_workflow')
    try:
        wtool.doActionFor(content, 'publish_internally')
    except WorkflowException:
        pass # Content has already been published


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
    if layout != "timeline_view":
        site.setLayout("timeline_view")
        LOG.info("set timeline_view as default page")
