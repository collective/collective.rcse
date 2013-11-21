from zope.component.interfaces import ObjectEvent
from zope.component.interfaces import IObjectEvent
from zope import interface


class IRequestAddedEvent(IObjectEvent):
    pass


class RequestAddedEvent(ObjectEvent):
    interface.implements(IRequestAddedEvent)


class IRequestValidatedEvent(IObjectEvent):
    pass


class RequestValidatedEvent(ObjectEvent):
    interface.implements(IRequestValidatedEvent)


class IRequestRefusedEvent(IObjectEvent):
    pass


class RequestRefusedEvent(ObjectEvent):
    interface.implements(IRequestRefusedEvent)
