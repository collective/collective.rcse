from zope import interface
from plonetheme.foundation.browser.layer import Layer as FoundationLayer
from plonetheme.jquerymobile.layer import Layer as JQMobileLayer
from plone.app.discussion.interfaces import IDiscussionLayer


class CommonLayer(interface.Interface):
    """Marker interface which is used in both theme"""


class MobileLayer(CommonLayer, JQMobileLayer, IDiscussionLayer):
    """Marker interface which is used in the mobile theme."""


class DesktopLayer(CommonLayer, FoundationLayer, IDiscussionLayer):
    """Marker interface which is used in the desktop theme"""
