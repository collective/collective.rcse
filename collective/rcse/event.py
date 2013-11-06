from zope import interface
from zope import schema


class IUserRolesModifiedOnObjectEvent(interface.Interface):
    """An event related to user having new roles on an object."""
    username = schema.ASCIILine(
        title=u"Username"
        )
    object = interface.Attribute(u"The object on which the user has new roles")


class UserRolesModifiedOnObjectEvent(object):
    interface.implements(IUserRolesModifiedOnObjectEvent)

    def __init__(self, username, object):
        self.username = username
        self.object = object
