from plone.autoform import directives as form
from plone.app.textfield import RichText
from plone.namedfile import field
from plone.supermodel import model
from z3c.form.browser.select import SelectFieldWidget
from zope import interface
from zope import schema

from collective.rcse.i18n import _
from collective.rcse.i18n import _t
from collective.rcse.content import vocabularies


class IMember(model.Schema):
    """This is a high level schema of info"""

    model.fieldset(
        'personal',
        label=_(u'Personal information'),
        fields=[
            'gender',
            'bio',
            'lang',
            'birthdate',
            'avatar',
            'areas_of_expertise',
            'interests',
            ]
        )

    model.fieldset(
        'contact',
        label=_(u'Contact information'),
        fields=[
            'professional_email',
            'personal_email',
            'professional_mobile_phone',
            'personal_mobile_phone',
            'professional_landline_phone',
            'personal_landline_phone',
            'skype',
            'website',
            'blog',
            'viadeo',
            'linkedin',
            'google',
            'twitter',
            ]
        )

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

    company = schema.ASCIILine(
        title=_t(u"Company")
    ) # ID
    function = schema.TextLine(
        title=_t(u"Function"),
    )

    bio = RichText(
        title=_t(u"Presentation"),
        required=False
    )
    form.widget('lang', SelectFieldWidget, multiple="multiple")
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
        vocabulary=vocabularies.gender,
        required=False
    )
    avatar = field.NamedBlobImage(
        title=_t(u"Avatar"),
        required=False
    )

    areas_of_expertise = schema.List(
        title=_t(u"Areas of expertise"),
        value_type=schema.TextLine(
            title=_t(u"Expertise"),
        ),
        required=False
    )
    interests = schema.List(
        title=_t(u"Interests"),
        value_type=schema.TextLine(
            title=_t(u"Interest"),
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
        title=_t(u"Personal mobile phone"),
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
        title=_t(u"Skype"),
        required=False
    )

    website = schema.URI(title=_t(u"Website"), required=False)
    blog = schema.URI(title=_t(u"Blog"), required=False)
    viadeo = schema.URI(title=_t(u"Viadeo"), required=False)
    linkedin = schema.URI(title=_t(u"LinkedIn"), required=False)
    google = schema.URI(title=_t(u"Google+"), required=False)
    twitter = schema.URI(title=_t(u"Twitter"), required=False)
