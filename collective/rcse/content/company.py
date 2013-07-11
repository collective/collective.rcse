from plone.namedfile import field
from zope import interface
from zope import schema

from collective.rcse.i18n import _t
from collective.rcse.content import vocabularies


class ICompany(interface.Interface):
    """Schema for the dexterity company content type."""
    corporate_name = schema.TextLine(
        title=_t(u"Corporate name")
    )
    sector = schema.Choice(
        title=_t(u"Sector"),
        vocabulary=vocabulary.sector
    )
    service = schema.TextLine(
        title=_t(u"Service"),
        required=False
    )
    logo = field.NamedBlobImage(
        title=_t(u"Logo"),
        required=False
    )
    address = schema.TextLine(
        title=_t(u"Address"),
        required=False
    )
    postal_code = schema.TextLine(
        title=_t(u"Postal code")
    )
    city = schema.TextLine(
        title=_t(u"City")
    )
    website = schema.TextLine(
        title=_t(u"Website"),
        required=False
    )
    blog = schema.TextLine(
        title=_t(u"Blog"),
        required=False
    )
    turnover = schema.TextLine(
        title=_t(u"Turnover"),
        required=False
    )
