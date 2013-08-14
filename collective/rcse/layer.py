from zope import interface
from plonetheme.foundation.browser.layer import Layer as FoundationLayer
from plonetheme.jquerymobile.layer import Layer as JQMobileLayer
from plone.app.discussion.interfaces import IDiscussionLayer
from collective.favoriting.layer import Layer as FavLayer
from plone.app.event.interfaces import IBrowserLayer as EventLayer

class CommonLayer(FavLayer, IDiscussionLayer, EventLayer):
    """Marker interface which is used in both theme"""


class MobileLayer(CommonLayer, JQMobileLayer):
    """Marker interface which is used in the mobile theme."""


class DesktopLayer(CommonLayer, FoundationLayer):
    """Marker interface which is used in the desktop theme"""
