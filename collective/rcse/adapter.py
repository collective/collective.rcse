from zope import component
from zope import interface

from cioppino.twothumbs.event import ILikeEvent
from cioppino.twothumbs.event import IUnlikeEvent
from cioppino.twothumbs.event import IDislikeEvent
from cioppino.twothumbs.event import IUndislikeEvent
from collective.favoriting.event import IAddedToFavoritesEvent
from collective.favoriting.event import IRemovedFromFavoritesEvent
from collective.history.adapter import IExtractWhat

from collective.history.i18n import _ as _h


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
    what = _h(u'added to his favorites:')


class FavoritingRemovedFromFavorites(BaseHistoryAdapter):
    component.adapts(IRemovedFromFavoritesEvent)
    what = _h(u'remove from his favorites:')
