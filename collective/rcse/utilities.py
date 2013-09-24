from OFS.SimpleItem import SimpleItem
from plone.dexterity import utils
from Products.CMFPlone.utils import getToolByName
from Products.membrane.interfaces import IUserAdder
from zope import interface
from zope.component.hooks import getSite
from zope.globalrequest import getRequest

from collective.rcse.utils import sudo
from collective.rcse.page.controller.person_view import GetMemberInfoView
from collective.whathappened.utility import IDisplay
from collective.whathappened.i18n import _ as _w


class RcseUserAdder(SimpleItem):
    """Used by Products.membrane when a user is added."""
    interface.implements(IUserAdder)

    def addUser(self, login, password):
        self.mtool = getToolByName(self, 'membrane_tool')
        results = self.mtool.searchResults(getUserName=login)
        if len(results) > 0:
            return
        self._createUser(login)

    @sudo()
    def _createUser(self, username):
        container = self.unrestrictedTraverse('users_directory')
        item = utils.createContentInContainer(
            container,
            'collective.rcse.member',
            checkConstraints=False,
            username=username)
        item.manage_setLocalRoles(username, ['Owner'])
        item.reindexObjectSecurity()


class BaseDisplay(object):
    """Used by collective.whathappened to display notifications."""
    interface.implements(IDisplay)

    def display(self, context, request, notification):
        where = notification.where.encode('utf-8')
        self.what = notification.what
        if context is not None:
            try:
                title = context.restrictedTraverse(where).Title()
            except KeyError:
                self.where = where.split('/')[-1]
            else:
                self.where = title.decode('utf-8')
        else:
            self.where = where.split('/')[-1]
        for index, who in enumerate(notification.who):
            user = GetMemberInfoView(getSite(), request)
            user(who)
            if user is not None and user.fullname is not None:
                notification.who[index] = user.fullname
        self.who = ', '.join(notification.who)
        self.plural = True if len(notification.who) > 1 else False
        if self.plural:
            return _w(u"${who} have ${what} ${where}",
                     mapping={'who': self.who,
                              'what': self.what,
                              'where': self.where
                              })
        else:
            return _w(u"${who} has ${what} ${where}",
                     mapping={'who': self.who,
                              'what': self.what,
                              'where': self.where
                              })


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
