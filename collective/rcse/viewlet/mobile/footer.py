from zope import component
from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry


class FooterLinks(ViewletBase):
    """display the themeswitcher link"""

    def get_theme(self):
        registry = component.queryUtility(IRegistry)
        key = "collective.themeswitcher.theme.desktop"
        return registry.get(key, "collective.rcse.desktop")
