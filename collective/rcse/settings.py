import os
from Products.CMFCore.utils import getToolByName
from zope import component
from zope import interface
from zope import schema

from collective.rcse.i18n import _


class ISettings(interface.Interface):
    """Marker interface to get utilities giving
    interfaces with default settings."""

    def getInterface():
        """Return an interface with default settings."""


class IPersonalPreferences(interface.Interface):
    """Settings for user preferences. See registry.xml for more details."""

    subscribe_when_favorited = schema.Bool(
        title=_(u"Subscribe when favorited"),
        description=_(u"You will automatically subscribed to contents "
                      u"you add to your favorites."),
        default=True
    )
    watch_when_favorited = schema.Bool(
        title=_(u"Watch when favorited"),
        description=_(u"You will automatically watch groups you add "
                      u"to your favorites."),
        default=True
    )


def getDefaultSettings():
    settings = {}
    for name, description in IPersonalPreferences.namesAndDescriptions():
        settings[name] = description.default
    utilities = component.getUtilitiesFor(ISettings)
    for name, utility in utilities:
        interface = utility.getInterface()
        for name, description in interface.namesAndDescriptions():
            settings[name] = description.default
    return settings


FEATURES = (
    "breadcrumb",
)

class Features(object):
    def __init__(self):
        self.environ = os.environ
        #Validated features are simple attribute not listed in FEATURES
        #self.my_validated_feature = True

    def __getattribute__(self, name):
        if name in FEATURES:
            return bool(self.environ.get("rcse_features_%s" % name, False))
        return object.__getattribute__(self, name)

features = Features()
