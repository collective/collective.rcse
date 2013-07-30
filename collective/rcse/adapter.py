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

    def __init__(self, event):
        self.event = event


class CioppinoLike(BaseHistoryAdapter):
    component.adapts(ILikeEvent)

    def __call__(self):
        return _(u'liked'), {}


class CioppinoUnlike(BaseHistoryAdapter):
    component.adapts(IUnlikeEvent)

    def __call__(self):
        return _(u'unliked'), {}


class CioppinoDislike(BaseHistoryAdapter):
    component.adapts(IDislikeEvent)

    def __call__(self):
        return _(u'disliked'), {}


class CioppinoUndislike(BaseHistoryAdapter):
    component.adapts(IUndislikeEvent)

    def __call__(self):
        return _(u'undisliked'), {}


class FavoritingAddedToFavorites(BaseHistoryAdapter):
    component.adapts(IAddedToFavoritesEvent)

    def __call__(self):
        return _(u'added to his favorites:'), {}


class FavoritingRemovedFromFavorites(BaseHistoryAdapter):
    component.adapts(IRemovedFromFavoritesEvent)

    def __call__(self):
        return _(u'remove from his favorites:'), {}


