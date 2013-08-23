from Products.membrane.interfaces import IUserAdder
from zope import interface

from collective.whathappened.utility import IDisplay
from collective.whathappened.i18n import _ as _w


class RcseUserAdder(object):
    """Used by Products.membrane when a user is added."""
    interface.implements(IUserAdder)

    def addUser(self, login, password):
        import pdb; pdb.set_trace()


class BaseDisplay(object):
    """Used by collective.whathappened to display notifications."""
    interface.implements(IDisplay)

    def display(self, context, request, notification):
        where = notification.where.encode('utf-8')
        try:
            title = context.restrictedTraverse(where).Title()
            self.where = title.decode('utf-8')
        except KeyError:
            self.where = where.split('/')[-1]
        self.who = ', '.join(notification.who)
        self.plural = True if len(notification.who) > 1 else False


class LikedDisplay(BaseDisplay):
    def display(self, context, request, notification):
        super(LikedDisplay, self).display(context, request, notification)
        if self.plural:
            return _w(u"${who} like ${where}",
                      mapping={'who': self.who,
                               'where': self.where})
        else:
            return _w(u"${who} likes ${where}",
                      mapping={'who': self.who,
                               'where': self.where})


class DislikedDisplay(BaseDisplay):
    def display(self, context, request, notification):
        super(DislikedDisplay, self).display(context, request, notification)
        if self.plural:
            return _w(u"${who} dislike ${where}",
                      mapping={'who': self.who,
                               'where': self.where})
        else:
            return _w(u"${who} dislikes ${where}",
                      mapping={'who': self.who,
                               'where': self.where})


class UnlikedDisplay(BaseDisplay):
    def display(self, context, request, notification):
        super(UnlikedDisplay, self).display(context, request, notification)
        if self.plural:
            return _w(u"${who} do not like ${where} anymore",
                      mapping={'who': self.who,
                               'where': self.where})
        else:
            return _w(u"${who} does not like ${where} anymore",
                      mapping={'who': self.who,
                               'where': self.where})


class UndislikedDisplay(BaseDisplay):
    def display(self, context, request, notification):
        super(UndislikedDisplay, self).display(context, request, notification)
        if self.plural:
            return _w(u"${who} do not dislike ${where} anymore",
                      mapping={'who': self.who,
                               'where': self.where})
        else:
            return _w(u"${who} does not dislike ${where} anymore",
                      mapping={'who': self.who,
                               'where': self.where})


class FavoritedDisplay(BaseDisplay):
    def display(self, context, request, notification):
        super(FavoritedDisplay, self).display(context, request, notification)
        if self.plural:
            return _w(u"${who} have added ${where} to their favorites",
                      mapping={'who': self.who,
                               'where': self.where})
        else:
            return _w(u"${who} has added ${where} to his favorites",
                      mapping={'who': self.who,
                               'where': self.where})


class UnfavoritedDisplay(BaseDisplay):
    def display(self, context, request, notification):
        super(UnfavoritedDisplay, self).display(context, request, notification)
        if self.plural:
            return _w(u"${who} have removed ${where} from their favorites",
                      mapping={'who': self.who,
                               'where': self.where})
        else:
            return _w(u"${who} has removed ${where} from his favorites",
                      mapping={'who': self.who,
                               'where': self.where})
