from zope import interface
from zope import schema


class IUserAddRolesOnObjectEvent(interface.Interface):
    """An event related to user having new roles on an object."""
    username = schema.ASCIILine(
        title=u"Username"
        )
    roles = schema.List(
        title=u"Roles",
        value_type=schema.ASCIILine()
        )
    object = interface.Attribute(u"The object on which the user has new roles")


class UserAddRolesOnObjectEvent(object):
    interface.implements(IUserAddRolesOnObjectEvent)

    def __init__(self, username, roles, object):
        self.username = username
        self.roles = roles
        self.object = object
