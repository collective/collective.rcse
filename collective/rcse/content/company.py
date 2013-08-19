from plone.namedfile import field
from zope import interface
from zope import schema

from collective.rcse.i18n import _


class ICompany(interface.Interface):
    """Schema for the dexterity company content type."""
    logo = field.NamedBlobImage(
        title=_(u"Logo"),
        required=False
    )
    corporate_name = schema.TextLine(
        title=_(u"Corporate name")
    )
    sector = schema.TextLine(
        title=_(u"Sector"),
    )
    service = schema.TextLine(
        title=_(u"Service"),
        required=False
    )
    turnover = schema.TextLine(
        title=_(u"Turnover"),
        required=False
    )
    address = schema.TextLine(
        title=_(u"Address"),
        required=False
    )
    postal_code = schema.TextLine(
        title=_(u"Postal code")
    )
    sites = schema.List(
        title=_(u"Sites"),
        value_type=schema.TextLine(),
        required=False
        )
    city = schema.TextLine(
        title=_(u"City")
    )
    website = schema.TextLine(
        title=_(u"Website"),
        required=False
    )
    blog = schema.TextLine(
        title=_(u"Blog"),
        required=False
    )
