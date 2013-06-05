from zope import interface
from zope import schema
from collective.rcse.i18n import _


class PersonInfo(interface.Interface):
    """This is a high level schema of info"""
    #ID
    url = schema.URI(title=_(u"URL"))
    uid = schema.TextLine(title=_(u"UID"))

    #name
    short_name = schema.TextLine(title=_(u"Short Name"), required=False)
    first_name = schema.TextLine(title=_(u"First Name"))
    last_name = schema.TextLine(title=_(u"Last Name"))
    formated_name = schema.TextLine(title=_(u"Formated Name"))
#    sex = schema.Choice(title=u"Sex",
#                        vocabulary="collective.rcse.vocab.sex")

    #about
    about = schema.Text(title=_(u"About me"), required=False)
    birthdate = schema.TextLine(title=_(u"Birth Date"), required=False)
    lang = schema.ASCIILine(title=_(u"Main spoken language"), required=False)
    photo = schema.URI(title=_(u"Photo URL"), required=False)

    #organisation
    organization = schema.TextLine(title=_(u"Orgnization"))
    title = schema.TextLine(title=_(u"Title"))

    #contact
    email_pro = schema.ASCIILine(title=_(u"Email address (pro)"))
    email_perso = schema.ASCIILine(title=_(u"Email address (perso)"))
    phone = schema.ASCIILine(title=_(u"Phone number"), required=False)
    mobile = schema.ASCIILine(title=_(u"Mobile phone number"), required=False)

    #social things
    website = schema.URI(title=_(u"Website"), required=False)
    blog = schema.URI(title=_(u"Blog"), required=False)
    twitter = schema.ASCIILine(title=_(u"Twitter ID"), required=False)
    skype = schema.ASCIILine(title=_(u"Skype ID"), required=False)
    gplus = schema.URI(title=_(u"Google+ URL"), required=False)
    linkedin = schema.URI(title=_(u"Linkedin URL"), required=False)
    viadeo = schema.URI(title=_(u"Viadeo URL"), required=False)
