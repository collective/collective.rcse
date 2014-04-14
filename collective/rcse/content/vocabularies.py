from plone.app.uuid.utils import uuidToObject
from plone.i18n.normalizer.base import baseNormalize
from plone.memoize import ram
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from zope.component.hooks import getSite

from collective.rcse.i18n import _, _t
from collective.rcse import cache
from collective.rcse.settings import IPersonalPreferences, themes as s_themes


themes = s_themes

gender = SimpleVocabulary([
    SimpleTerm(value=u"female", title=_(u"Female")),
    SimpleTerm(value=u"male", title=_(u"Male")),
])


languages = SimpleVocabulary([
    SimpleTerm(value=u"English", title=_(u"English")),
    SimpleTerm(value=u"French", title=_(u"French")),
    SimpleTerm(value=u"Italian", title=_(u"Italian")),
    SimpleTerm(value=u"Spanish", title=_(u"Spanish")),
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


def addableTypes(context):
    blacklist = ['collective.rcse.proxygroup', 'collective.rcse.audio']
    vocabulary = getUtility(IVocabularyFactory,
                            name="plone.app.vocabularies.UserFriendlyTypes")
    types = list(vocabulary(context))
    terms = [t for t in types if t.token not in blacklist]
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
    companies = catalog.unrestrictedSearchResults(**query)
    terms = [SimpleTerm(value=company.id, title=company.Title)
             for company in companies]
    return SimpleVocabulary(terms)


@ram.cache(cache.getCacheKeyGroupTitle)
def _getGroupTitleFromUUID(uuid):
    group = uuidToObject(uuid)
    if group is None:
        cache.clearCacheKeyGroupTitleFromUUID(uuid)
        return ''
    return group.title


@ram.cache(cache.getCacheKeyGroupAddPermission)
def _getGroupsWithAddPermission(username):
    site = getSite()
    portal_membership = getToolByName(site, 'portal_membership')
    catalog = getToolByName(site, 'portal_catalog')
    query = {"portal_type": "collective.rcse.group",
             "sort_on": "sortable_title"}
    terms = []
    brains = catalog(**query)
    for brain in brains:
        if portal_membership.checkPermission('Add portal content',
                                             brain.getObject()):
            terms.append(brain.UID)
    return terms


def groups(context):
    """Group where the user can add contents."""
    portal_membership = getToolByName(context, 'portal_membership')
    username = portal_membership.getAuthenticatedMember().getUserName()
    uids = _getGroupsWithAddPermission(username)
    terms = []
    for uid in uids:
        terms.append(SimpleVocabulary.createTerm(
                unicode(uid),
                str(uid),
                _getGroupTitleFromUUID(uid)
                ))
    return SimpleVocabulary(terms)


def groups_with_home(context):
    """Group where the user can add contents + home."""
    portal_membership = getToolByName(context, 'portal_membership')
    username = portal_membership.getAuthenticatedMember().getUserName()
    site = getToolByName(context, 'portal_url').getPortalObject()
    home = site['home']
    terms = [SimpleTerm(value=IUUID(home), title=_(u"Home"))]
    uids = _getGroupsWithAddPermission(username)
    for uid in uids:
        terms.append(SimpleVocabulary.createTerm(
                unicode(uid),
                str(uid),
                _getGroupTitleFromUUID(uid)
                ))
    return SimpleVocabulary(terms)


settings = SimpleVocabulary([
    SimpleTerm(value=field[0], title=field[1].title)
    for field in IPersonalPreferences.namesAndDescriptions()
])
