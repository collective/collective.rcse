from zope.i18n import translate
from zope import component
from zope import interface

from cioppino.twothumbs.event import ILikeEvent
from cioppino.twothumbs.event import IUnlikeEvent
from cioppino.twothumbs.event import IDislikeEvent
from cioppino.twothumbs.event import IUndislikeEvent
from collective.favoriting.event import IAddedToFavoritesEvent
from collective.favoriting.event import IRemovedFromFavoritesEvent
from collective.history.adapter import IExtractWhat

from collective.rcse.i18n import _


class BaseHistoryAdapter(object):
    interface.implements(IExtractWhat)

    what = u''
    what_info = {}

    def __init__(self, event):
        self.event = event

    def __call__(self):
        return translate(_(self.what)), self.what_info


class CioppinoLike(BaseHistoryAdapter):
    component.adapts(ILikeEvent)
    what = u'liked'


class CioppinoUnlike(BaseHistoryAdapter):
    component.adapts(IUnlikeEvent)
    what = u'unliked'


class CioppinoDislike(BaseHistoryAdapter):
    component.adapts(IDislikeEvent)
    what = u'disliked'


class CioppinoUndislike(BaseHistoryAdapter):
    component.adapts(IUndislikeEvent)
    what = u'undisliked'


class FavoritingAddedToFavorites(BaseHistoryAdapter):
    component.adapts(IAddedToFavoritesEvent)
    what = u'added to his favorites:'


class FavoritingRemovedFromFavorites(BaseHistoryAdapter):
    component.adapts(IRemovedFromFavoritesEvent)
    what = u'remove from his favorites:'
