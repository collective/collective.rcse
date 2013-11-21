from zope import component
from zope import interface
from zope.schema.interfaces import IVocabularyFactory
from plone.registry.interfaces import IRegistry
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from plone.i18n.normalizer.base import baseNormalize
from zope.i18n import translate
from zope.globalrequest import getRequest
from collective.requestaccess.i18n import _


class RegistryVocabulary(object):
    """vocabulary to use with plone.app.registry"""
    interface.implements(IVocabularyFactory)

    def __init__(self, key):
        self.key = key

    def __call__(self, context):

        registry = component.queryUtility(IRegistry)
        if registry is None:
            return []
        categories = registry[self.key]
        terms = [
            SimpleTerm(
                baseNormalize(category),
                baseNormalize(category),
                self.translate(category)
            ) for category in categories
        ]
        return SimpleVocabulary(terms)

    def translate(self, msgid):
        request = getRequest()
        return translate(msgid, domain="plone", context=request)


role_vocab_key = 'collective.requestaccess.interfaces.Settings.roles'
RolesVocabulary = RegistryVocabulary(role_vocab_key)


def RequestTypes(context):
    return SimpleVocabulary([
        SimpleTerm("request", "request", _(u"Request")),
        SimpleTerm("invitation", "invitation", _(u"Invitation")),
    ])
