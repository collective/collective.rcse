from zope import interface
from plonetheme.jquerymobile.layer import Layer as JQMobileLayer
from plone.app.discussion.interfaces import IDiscussionLayer
from collective.favoriting.layer import Layer as FavLayer
from plone.app.event.interfaces import IBrowserLayer as EventLayer
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer



class CommonLayer(
    FavLayer, IDiscussionLayer, EventLayer,
    IPloneAppContenttypesLayer
):
    """Marker interface which is used in both theme"""


class MobileLayer(CommonLayer, JQMobileLayer):
    """Marker interface which is used in the mobile theme."""


class DesktopLayer(CommonLayer):
    """Marker interface which is used in the desktop theme"""
