from zope import schema
from zope import interface
from plone.app.textfield import RichText
from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.content import common

_ = RCSEMessageFactory

error_hour = _(u"Start hour can't be greater than end hour durint the same day")
error_day = _(u"start day can't be greater than end day")


def event_validation(ob):
    #fix sameday value
    if ob.start == ob.end:
        ob.sameday = True
    else:
        ob.sameday = False

    #start day >= end day
    if ob.start > ob.end:
        raise interface.Invalid(error_day)

    if ob.start_hour > ob.end_hour and ob.sameday:
        raise interface.Invalid(error_hour)


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

    sameday = schema.Bool(title=_(u"Same day"),
                          default=True,
                          readonly=True)

    interface.invariant(event_validation)
