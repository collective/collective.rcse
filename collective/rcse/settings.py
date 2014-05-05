import os
from zope import component
from zope import interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.rcse.i18n import _


class ISettings(interface.Interface):
    """Marker interface to get utilities giving
    interfaces with default settings."""

    def getInterface():
        """Return an interface with default settings."""


themes = SimpleVocabulary([
    SimpleTerm(value="", title=_(u"Default")),
    SimpleTerm(value="amelia", title=_(u"Amelia")),
    SimpleTerm(value="cerulean", title=_(u"Cerulean")),
    SimpleTerm(value="cosmo", title=_(u"Cosmo")),
    SimpleTerm(value="cyborg", title=_(u"Cyborg")),
    SimpleTerm(value="flatly", title=_(u"Flatly")),
    SimpleTerm(value="journal", title=_(u"Journal")),
    SimpleTerm(value="lumen", title=_(u"Lumen")),
#    SimpleTerm(value="readable", title=_(u"Readable")),
    SimpleTerm(value="simplex", title=_(u"Simplex")),
    SimpleTerm(value="slate", title=_(u"Slate")),
    SimpleTerm(value="spacelab", title=_(u"Spacelab")),
#    SimpleTerm(value="superhero", title=_(u"Superhero")),
    SimpleTerm(value="united", title=_(u"United")),
    SimpleTerm(value="yeti", title=_(u"Yeti")),
    ])


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
    receive_email_notifications = schema.Bool(
        title=_(u"Receive email notifications"),
        description=_(u"You will receive emails once a week if you have "
                      u"new notifications."),
        default=True
    )
    theme = schema.Choice(
        title=_(u"Theme"),
        description=_(u"You can choose a different theme."),
        default="",
        vocabulary=themes
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
