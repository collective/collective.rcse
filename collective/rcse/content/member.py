from plone.autoform import directives as form
from plone.app.textfield import RichText
from plone.memoize import ram
from plone.namedfile import field
from plone.supermodel import model
from z3c.form.browser.select import SelectFieldWidget
from zope import interface
from zope import schema

from collective.rcse.i18n import _
from collective.rcse.content import vocabularies
from collective.rcse.content.visibility import addVisibilityCheckbox
from Products.CMFCore.utils import getToolByName

import logging
from zope.schema.vocabulary import SimpleVocabulary

logger = logging.getLogger(__name__)


@addVisibilityCheckbox([
    'username',
    'company_id',
    'company',
    'email',
    'email_validation',
    'first_name',
    'last_name',
    'advertiser',
])
class IMember(model.Schema):
    """This is an interface to describe a member"""

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
        title=_(u"Username"),
        readonly=True
    )
    email = schema.TextLine(
        title=_(u"E-mail"),
        description=_(u"This is the email you will receive information on."
                      u" It will not be displayed to other users."),
        required=True,
    )
    email_validation = schema.ASCIILine(
        title=_("E-mail validation"),
        readonly=True,
        required=False
    )
    first_name = schema.TextLine(
        title=_(u"First Name"),
        required=True,
    )
    last_name = schema.TextLine(
        title=_(u"Last Name"),
        required=True,
    )

    company = schema.TextLine(
        title=_(u"Company"),
        readonly=True
    )
    company_id = schema.ASCIILine(
        title=_(u"Username"),
        readonly=True
    )
    function = schema.TextLine(
        title=_(u"Function"),
    )

    city = schema.TextLine(
        title=_(u"City"),
    )

    advertiser = schema.Bool(
        title=_(u"Advertiser")
    )

    bio = RichText(
        title=_(u"Presentation"),
        required=False
    )
    form.widget('lang', SelectFieldWidget, multiple="multiple")
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
        vocabulary=vocabularies.gender,
        required=False
    )
    avatar = field.NamedBlobImage(
        title=_(u"Avatar"),
        required=False
    )

    areas_of_expertise = schema.List(
        title=_(u"Areas of expertise"),
        value_type=schema.TextLine(
            title=_(u"Expertise"),
        ),
        required=False
    )
    interests = schema.List(
        title=_(u"Interests"),
        value_type=schema.TextLine(
            title=_(u"Interest"),
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
        title=_(u"Personal mobile phone"),
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
        title=_(u"Skype"),
        required=False
    )

    form.widget('website', placeholder=u"http://www.monsiteinternet.com")
    website = schema.URI(
        title=_(u"Website"), required=False,
        description=_(u"Don't forget http:// or https://"),
    )

    form.widget('blog', placeholder=u"http://www.monblog.com")
    blog = schema.URI(title=_(u"Blog"), required=False)

    form.widget('viadeo', placeholder=u"http://www.viadeo.com/profile/")
    viadeo = schema.URI(title=_(u"Viadeo"), required=False)

    form.widget('linkedin', placeholder=u"http://www.linkedin.com/profile/")
    linkedin = schema.URI(title=_(u"LinkedIn"), required=False)

    form.widget('google', placeholder=u"https://plus.google.com/")
    google = schema.URI(title=_(u"Google+"), required=False)

    form.widget('twitter', placeholder=u"https://twitter.com/")
    twitter = schema.URI(title=_(u"Twitter"), required=False)

    @interface.invariant
    def validate_urls(obj):
        viadeo = "http://www.viadeo.com/profile/"
        linkedin = "http://www.linkedin.com/profile/"
        google = "https://plus.google.com/"
        twitter = "https://twitter.com/"

        if obj.viadeo and not obj.viadeo.startswith(viadeo):
            raise interface.Invalid(
                _(u"${url} is not a valid ${service} url",
                  mapping={"url": obj.viadeo, "service": "viadeo"})
            )

        if obj.linkedin and not obj.linkedin.startswith(linkedin):
            raise interface.Invalid(
                _(u"${url} is not a valid ${service} url",
                  mapping={"url": obj.linkedin, "service": "linkedin"})
            )

        if obj.google and not obj.google.startswith(google):
            raise interface.Invalid(
                _(u"${url} is not a valid ${service} url",
                  mapping={"url": obj.google, "service": "google"})
            )

        if obj.twitter and not obj.twitter.startswith(twitter):
            raise interface.Invalid(
                _(u"${url} is not a valid ${service} url",
                  mapping={"url": obj.twitter, "service": "twitter"})
            )


def handle_member_added(context, event):
    logger.info('Member object added.')
    mtool = getToolByName(context, 'membrane_tool')
    mtool.indexObject(context)


def handle_member_modified(context, event):
    logger.info('Member object modified.')
    mtool = getToolByName(context, 'membrane_tool')
    mtool.reindexObject(context)


def handle_member_removed(context, event):
    logger.info('Member object removed.')
    mtool = getToolByName(context, 'membrane_tool')
    mtool.unindexObject(context)


def _members_cachekey(method, context, review_state):
    return review_state


@ram.cache(_members_cachekey)
def get_members_info(context, review_state="enabled"):
    query = {
        'sort_on': 'getId',  # because in mobile we need sorted results
        'portal_type': 'collective.rcse.member',
        'review_state': review_state
    }
    catalog = getToolByName(context, 'membrane_tool')
    brains = catalog(**query)
    userids = [brain.getUserId for brain in brains]

    def _getInfo(userid):
        person_view = context.restrictedTraverse('get_memberinfo')
        person_view(userid)
        return {
            "userid": userid,
            "dataid": person_view.get_membrane().getId(),
            "url": person_view.url,
            "photo": person_view.photo(),
            "email": person_view.email,
            "first_name": person_view.first_name,
            "last_name": person_view.last_name,
            "company": person_view.company,
            "function": person_view.function,
            "city": person_view.city,
        }
    members_info = map(_getInfo, userids)
    return members_info


def members_vocabulary(context):
    terms = []
    users = get_members_info(context, review_state="enabled")
    for user in users:
        try:
            display_name = u"%s %s - %s" % (user['first_name'],
                                            user['last_name'],
                                            user['company'])
            display_name = display_name.decode('utf-8')
        except UnicodeDecodeError as e:
            logger.error("%s %s" % (user['userid'], e))
            continue
        except UnicodeEncodeError as e:
            logger.error("%s %s" % (user['userid'], e))
            continue
        terms.append(SimpleVocabulary.createTerm(
            unicode(user['userid']),
            unicode(user['userid']),
            display_name,
        ))
    return SimpleVocabulary(terms)
