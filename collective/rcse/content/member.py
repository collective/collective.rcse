from plone.app.textfield import RichText
from plone.namedfile import field
from zope import interface
from zope import schema

from collective.rcse.i18n import _t
from collective.rcse.content import vocabularies


class IMember(interface.Interface):
    """This is a high level schema of info"""
    username = schema.ASCIILine(
        title=_t(u"Username"),
        readonly=True
    )
    email = schema.TextLine(
        title=_t(u"E-mail"),
        required=True,
    )
    first_name = schema.TextLine(
        title=_t(u"First Name"),
        required=True,
    )
    last_name = schema.TextLine(
        title=_t(u"Last Name"),
        required=True,
    )

    bio = RichText(
        title=_t(u"Presentation"),
        required=False
    )
    lang = schema.List(
        title=_t(u"Spoken languages"),
        required=False,
        value_type=schema.Choice(
            vocabulary=vocabularies.languages
        ),
    )
    birthdate = schema.Date(
        title=_t(u"Birthdate"),
        required=False
    )
    gender = schema.Choice(
        title=_t(u"Gender"),
        vocabulary=vocabularies.gender
    )
    avatar = field.NamedBlobImage(
        title=_t(u"Avatar"),
        required=False
    )

    company = schema.ASCIILine(
        title=_t(u"Company")
    ) # ID
    function = schema.Choice(
        title=_t(u"Function"),
        vocabulary=vocabularies.functions
    )

    areas_of_expertise = schema.List(
        title=_t(u"Areas of expertise"),
        value_type=schema.Choice(
            title=_t(u"Expertise"),
            vocabulary=vocabularies.areas_of_expertise
        ),
        required=False
    )
    interests = schema.List(
        title=_t(u"Interests"),
        value_type=schema.Choice(
            title=_t(u"Interest"),
            vocabulary=vocabularies.interests
        ),
        required=False
    )

    professional_email = schema.TextLine(
        title=_t(u"Professional e-mail"),
        required=False
    )
    personal_email = schema.TextLine(
        title=_t(u"Personal e-mail"),
        required=False
    )
    professional_mobile_phone = schema.TextLine(
        title=_t(u"Professional mobile phone"),
        required=False
    )
    personal_mobile_phone = schema.TextLine(
        title=_t(u"Professional e-mail"),
        required=False
    )
    professional_landline_phone = schema.TextLine(
        title=_t(u"Professional landline phone"),
        required=False
    )
    personal_landline_phone = schema.TextLine(
        title=_t(u"Personal landline phone"),
        required=False
    )
    skype = schema.TextLine(
        title=_t(u"Professional e-mail"),
        required=False
    )

    website = schema.URI(title=_t(u"Website"), required=False)
    blog = schema.URI(title=_t(u"Blog"), required=False)
    viadeo = schema.URI(title=_t(u"Viadeo"), required=False)
    linkedin = schema.URI(title=_t(u"LinkedIn"), required=False)
    google = schema.URI(title=_t(u"Google+"), required=False)
    twitter = schema.URI(title=_t(u"Twitter"), required=False)
