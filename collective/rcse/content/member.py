from plone.app.textfield import RichText
from plone.namedfile import field
from zope import interface
from zope import schema

from collective.rcse.i18n import _
from collective.rcse.content import vocabularies


class IMember(interface.Interface):
    """This is a high level schema of info"""
    username = schema.ASCIILine(
        title=_(u"Username"),
        readonly=True
    )
    email = schema.TextLine(
        title=_(u"E-mail"),
        required=True,
    )
    first_name = schema.TextLine(
        title=_(u"First Name"),
        required=True,
    )
    last_name = schema.TextLine(
        title=_(u"Last Name"),
        required=True,
    )

    bio = RichText(
        title=_(u"Presentation"),
        required=False
    )
    lang = schema.List(
        title=_(u"Spoken languages"),
        required=False,
        value_type=schema.Choice(
            vocabulary=vocabularies.languages
        ),
    )
    birthdate = schema.Date(
        title=_(u"Birthdate"),
        required=False
    )
    gender = schema.Choice(
        title=_(u"Gender"),
        vocabulary=vocabularies.gender
    )
    avatar = field.NamedBlobImage(
        title=_(u"Avatar"),
        required=False
    )

    company = schema.ASCIILine(
        title=_(u"Company")
    ) # ID
    function = schema.Choice(
        title=_(u"Function"),
        vocabulary=vocabularies.functions
    )

    areas_of_expertise = schema.List(
        title=_(u"Areas of expertise"),
        value_type=schema.Choice(
            title=_(u"Expertise"),
            vocabulary=vocabularies.areas_of_expertise
        ),
        required=False
    )
    interests = schema.List(
        title=_(u"Interests"),
        value_type=schema.Choice(
            title=_(u"Interest"),
            vocabulary=vocabularies.interests
        ),
        required=False
    )

    professional_email = schema.TextLine(
        title=_(u"Professional e-mail"),
        required=False
    )
    personal_email = schema.TextLine(
        title=_(u"Personal e-mail"),
        required=False
    )
    professional_mobile_phone = schema.TextLine(
        title=_(u"Professional mobile phone"),
        required=False
    )
    personal_mobile_phone = schema.TextLine(
        title=_(u"Professional e-mail"),
        required=False
    )
    professional_landline_phone = schema.TextLine(
        title=_(u"Professional landline phone"),
        required=False
    )
    personal_landline_phone = schema.TextLine(
        title=_(u"Personal landline phone"),
        required=False
    )
    skype = schema.TextLine(
        title=_(u"Professional e-mail"),
        required=False
    )

    website = schema.URI(title=_(u"Website"), required=False)
    blog = schema.URI(title=_(u"Blog"), required=False)
    viadeo = schema.URI(title=_(u"Viadeo"), required=False)
    linkedin = schema.URI(title=_(u"LinkedIn"), required=False)
    google = schema.URI(title=_(u"Google+"), required=False)
    twitter = schema.URI(title=_(u"Twitter"), required=False)
