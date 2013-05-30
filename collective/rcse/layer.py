from plonetheme.foundation.browser.layer import Layer as FoundationLayer
from plonetheme.jquerymobile.layer import Layer as JQMobileLayer
from plone.app.discussion.interfaces import IDiscussionLayer


class MobileLayer(JQMobileLayer, IDiscussionLayer):
    """Marker interface which is used in the mobile theme."""


class DesktopLayer(FoundationLayer, IDiscussionLayer):
    """Marker interface which is used in the desktop theme"""
