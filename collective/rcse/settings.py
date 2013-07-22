from zope import interface
from zope import schema

from collective.rcse.i18n import _

class IDocumentActionsIcons(interface.Interface):
    """Interface for icon/actions mapping setting"""

    mapping = schema.Dict(
        title=_(u"Action to icon"),
        key_type=schema.ASCIILine(),
        value_type=schema.ASCIILine(),
    )
