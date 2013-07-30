from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope import interface
from zope import schema

from collective.rcse.i18n import _


class IDocumentActionsIcons(interface.Interface):
    """Interface for icon/actions mapping setting"""

    mapping = schema.Dict(
        title=_(u"Action to icon"),
        key_type=schema.ASCIILine(),
        value_type=schema.ASCIILine(),
    )


class IPersonalPreferences(interface.Interface):
    """Settings for user preferences. See registry.xml for more details."""

    subscribe_when_favorited = schema.Bool(
        title=_(u"Subscribe when favorited"),
        description=_(u"You will automatically subscribed to contents "
                      u"you add to your favorites."),
    )
    watch_when_favorited = schema.Bool(
        title=_(u"Watch when favorited"),
        description=_(u"You will automatically watch groups you add "
                      u"to your favorites."),
    )


def getUserSettings(context):
    """Return a dict with the authenticated user settings."""
    registry = getUtility(IRegistry)
    default_settings = registry.forInterface(IPersonalPreferences)
    settings = {}
    for s in IPersonalPreferences.names():
        try:
            settings[s] = default_settings.__getattr__(s)
        except AttributeError:
            settings[s] = None
    mtool = getToolByName(context, 'portal_membership')
    user = mtool.getAuthenticatedMember()
    if user is None:
        return settings
    #@TODO Think about a good way to get user settings (From Member content ?)
    return settings
