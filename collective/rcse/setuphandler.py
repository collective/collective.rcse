## setuphandlers.py
import logging
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.interfaces import IDexterityContainer


LOG = logging.getLogger("collective.history")


def setupVarious(context):
    """Create the history container"""

    if context.readDataFile('collective_rcse.txt') is None:
        return

    portal = context.getSite()
    updateWelcomePage(portal)
    createDirectories(portal)
    updateUsersDirectories(portal.users_directory)
    updateCompaniesDirectories(portal.companies_directory)


def createDirectories(parent):
    existing = parent.objectIds()
    if "users_directory" not in existing:
        _createObjectByType(
            "Folder",
            parent,
            id="users_directory",
            title="Users directory"
        )
    if "companies_directory" not in existing:
        _createObjectByType(
            "Folder",
            parent,
            id="companies_directory",
            title="Companies directory"
        )


def updateUsersDirectories(users_directory):
    #users_directory.setLayout("users_directory_view")
    aspect = ISelectableConstrainTypes(users_directory)
    addable = aspect.getImmediatelyAddableTypes()
    if "collective.rcse.member" not in addable:
        aspect.setConstrainTypesMode(1)  # select manually
        types = ["collective.rcse.member"]
        if IDexterityContainer.providedBy(users_directory):
            users_directory.immediately_addable_types = types
        else:
            aspect.setImmediatelyAddableTypes(types)


def updateCompaniesDirectories(companies_directory):
    #companies_directory.setLayout("companies_directory_view")
    aspect = ISelectableConstrainTypes(companies_directory)
    addable = aspect.getImmediatelyAddableTypes()
    if "collective.rcse.company" not in addable:
        aspect.setConstrainTypesMode(1)  # select manually
        types = ["collective.rcse.company"]
        if IDexterityContainer.providedBy(companies_directory):
            users_directory.immediately_addable_types = types
        else:
            aspect.setImmediatelyAddableTypes(types)


def updateWelcomePage(site):
    layout = site.getLayout()
    if layout != "welcome_view":
        site.setLayout("welcome_view")
        LOG.info("set welcome_view as default page")
