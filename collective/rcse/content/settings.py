from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation import factory
from zope import component
from zope import interface
from zope import schema

from collective.rcse.settings import getDefaultSettings


class ISettings(interface.Interface):
    settings = schema.Dict(
        title=u"Settings",
        key_type=schema.ASCIILine(),
        value_type=schema.ASCIILine()
    )


class Settings(object):
    interface.implements(ISettings)
    component.adapts(IAttributeAnnotatable)

    def __init__(self):
        self.settings = getDefaultSettings()


SettingsFactory = factory(Settings)
