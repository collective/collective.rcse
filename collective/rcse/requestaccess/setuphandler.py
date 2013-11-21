## setuphandlers.py
import logging

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.interfaces import IDexterityContainer
from Products.CMFCore.utils import getToolByName

LOG = logging.getLogger("collective.requestaccess")


def setupVarious(context):
    """Create the request/invite container"""

    if context.readDataFile('collective_requestaccess.txt') is None:
        return

