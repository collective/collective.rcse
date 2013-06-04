from zope import schema
from plone.directives import form
from plone.app.textfield import RichText
from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.content import common

_ = RCSEMessageFactory


class EventSchema(common.RCSEContent):
    """A conference session. Sessions are managed inside Programs.
    """

    start = schema.Date(title=_(u"Start date"))
    end = schema.Date(title=_(u"End date"),
                      required=False)

    start_hour = schema.Time(title=_(u"Start hour"),
                             required=False)
    end_hour = schema.Time(title=_(u"End hour"),
                           required=False)

    text = RichText(title=_(u"Text"),
                    required=False)

    event_url = schema.URI(title=_(u"Event URL"),
                           required=False)
