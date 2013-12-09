from Acquisition import aq_inner

from zope import component
from zope import interface
from zope.globalrequest import getRequest

from plone.app.contenttypes import indexers
from plone.indexer.decorator import indexer
from Products.CMFPlone.utils import getToolByName

from cioppino.twothumbs.event import ILikeEvent
from cioppino.twothumbs.event import IUnlikeEvent
from cioppino.twothumbs.event import IDislikeEvent
from cioppino.twothumbs.event import IUndislikeEvent
from collective.etherpad import etherpad_view
from collective.favoriting.event import IAddedToFavoritesEvent
from collective.favoriting.event import IRemovedFromFavoritesEvent
from collective.history.extract import IExtractWhat
from collective.history.i18n import _ as _h
from collective.rcse.content import etherpad


class BaseHistoryAdapter(object):
    interface.implements(IExtractWhat)

    what = u''
    what_info = {}

    def __init__(self, event):
        self.event = event

    def __call__(self):
        return self.what, self.what_info


class CioppinoLike(BaseHistoryAdapter):
    component.adapts(ILikeEvent)
    what = _h(u'liked')


class CioppinoUnlike(BaseHistoryAdapter):
    component.adapts(IUnlikeEvent)
    what = _h(u'unliked')


class CioppinoDislike(BaseHistoryAdapter):
    component.adapts(IDislikeEvent)
    what = _h(u'disliked')


class CioppinoUndislike(BaseHistoryAdapter):
    component.adapts(IUndislikeEvent)
    what = _h(u'undisliked')


class FavoritingAddedToFavorites(BaseHistoryAdapter):
    component.adapts(IAddedToFavoritesEvent)
    what = _h(u'favorited')


class FavoritingRemovedFromFavorites(BaseHistoryAdapter):
    component.adapts(IRemovedFromFavoritesEvent)
    what = _h(u'unfavorited')


#we need to query the catalog to get content where current user has localroles.
@indexer(interface.Interface)
def user_with_local_roles(context):
    context = aq_inner(context)
    local_roles = context.get_local_roles()
    users = set()

    for user, roles in local_roles:
        users.add(user)

    return list(users)


@indexer(etherpad.EtherpadSchema)
def SearchableText_etherpad(context):
    view = etherpad_view.EtherpadView(context, getRequest())
    view.update()
    if view.etherpad is None:
        return indexers.SearchableText(context)
    text = indexers.SearchableText(context)
    transforms = getToolByName(context, 'portal_transforms')
    value = str(view.content())
    content = transforms.convertTo('text/plain', value, mimetype='text/html')
    return indexers._unicode_save_string_concat(text, content.getData())
