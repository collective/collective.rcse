from plonetheme.foundation.browser.layer import Layer as FoundationLayer
from plonetheme.jquerymobile.layer import Layer as JQMobileLayer


class MobileLayer(JQMobileLayer):
    """Marker interface which is used in the mobile theme."""


class DesktopLayer(FoundationLayer):
    """Marker interface which is used in the desktop theme"""
