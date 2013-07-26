from plone.i18n.normalizer.base import baseNormalize
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.rcse.i18n import _, _t


gender = SimpleVocabulary([
    SimpleTerm(value=u"female", title=_(u"Female")),
    SimpleTerm(value=u"male", title=_(u"Male")),
])

languages = SimpleVocabulary([
    SimpleTerm(value=u"English", title=_t(u"English")),
    SimpleTerm(value=u"French", title=_t(u"French")),
    SimpleTerm(value=u"Italian", title=_t(u"Italian")),
    SimpleTerm(value=u"Spanish", title=_t(u"Spanish")),
])


def groupTypes(context):
    """Get content types addable in a specific context"""
    portal_types = getToolByName(context, 'portal_types')
    types = portal_types.listContentTypes()
    types = [t for t in types if context.getTypeInfo().allowType(t)]
    terms = [
        SimpleTerm(
            baseNormalize(t),
            baseNormalize(t),
            _(portal_types[t].title)
            ) for t in sorted(types)
        ]
    return SimpleVocabulary(terms)

sortBy = SimpleVocabulary([
    SimpleTerm('relevance', 'relevance', _(u'Relevance')),
    SimpleTerm('Date', 'Date', _(u'Date')),
    SimpleTerm('sortable_title', 'sortable_title', _(u'Title')),
    ])
