from plone.i18n.normalizer.base import baseNormalize
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.rcse.i18n import _, _t
from collective.rcse.settings import IPersonalPreferences

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


def companies(context):
    catalog = getToolByName(context, 'portal_catalog')
    query = {'portal_type': 'collective.rcse.company',
             'sort_on': 'sortable_title'}
    companies = catalog(**query)
    terms = [SimpleTerm(value=company.id, title=company.Title)
             for company in companies]
    terms += [
        SimpleTerm(value=u"__new_company",
                   title=_(u"Create a new company"))
        ]
    return SimpleVocabulary(terms)


def groups(context):
    catalog = getToolByName(context, 'portal_catalog')
    query = {"portal_type": "collective.rcse.group",
             "sort_on": "sortable_title"}
    terms = []
    brains = catalog(**query)
    for brain in brains:
        terms.append(SimpleVocabulary.createTerm(
            unicode(brain.UID),
            str(brain.UID),
            brain.Title
        ))
    return SimpleVocabulary(terms)


def groups_with_home(context):
    catalog = getToolByName(context, 'portal_catalog')
    query = {"portal_type": "collective.rcse.group",
             "sort_on": "sortable_title"}
    site = getToolByName(context, 'portal_url').getPortalObject()
    home = site['home']
    terms = [SimpleTerm(value=IUUID(home), title=_(u"Home"))]
    brains = catalog(**query)
    for brain in brains:
        terms.append(SimpleVocabulary.createTerm(
            unicode(brain.UID),
            str(brain.UID),
            brain.Title
        ))
    return SimpleVocabulary(terms)


settings = SimpleVocabulary([
        SimpleTerm(value=field[0], title=field[1].title)
        for field in IPersonalPreferences.namesAndDescriptions()
        ])
