from AccessControl.SecurityManagement import newSecurityManager,\
    getSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from OFS.SimpleItem import SimpleItem
from plone.dexterity import utils
from Products.CMFPlone.utils import getToolByName
from Products.membrane.interfaces import IUserAdder
from zope import interface

from collective.whathappened.utility import IDisplay
from collective.whathappened.i18n import _ as _w


class RcseUserAdder(SimpleItem):
    """Used by Products.membrane when a user is added."""
    interface.implements(IUserAdder)

    def addUser(self, login, password):
        self._createUser(login)

    def _createUser(self, username):
        container = self.unrestrictedTraverse('users_directory')
        self.mtool = getToolByName(self, 'membrane_tool')
        results = self.mtool.searchResults(getUserName=username)
        if len(results) > 0:
            return
        self._security_manager = getSecurityManager()
        self._sudo('Manager')
        item = utils.createContentInContainer(
            container,
            'collective.rcse.member',
            checkConstraints=False,
            username=username)
        item.manage_setLocalRoles(username, ['Owner'])
        item.reindexObjectSecurity()
        self._sudo()

    def _sudo(self, role=None):
        """Give admin power to the current call"""
        if role is not None:
            if self.mtool.getAuthenticatedMember().has_role(role):
                return
            sm = getSecurityManager()
            acl_users = getToolByName(self, 'acl_users')
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', [role], ''
            )
            tmp_user = tmp_user.__of__(acl_users)
            newSecurityManager(None, tmp_user)
        else:
            setSecurityManager(self._security_manager)


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
