from zope import interface
from plonetheme.foundation.browser.layer import Layer


class MobileLayer(interface.Interface):
    """Marker interface which is used in the mobile theme."""


class DesktopLayer(Layer):
    """Marker interface which is used in the desktop theme"""
