from zope import schema
from plone.directives import form
from Products.Five.browser import BrowserView
from plone.app.textfield import RichText
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class EventSchema(form.Schema):
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


class EventView(BrowserView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        pass

    def sameday(self):
        if self.context.end is None:
            return True
        sameday = self.context.start == self.context.end
        has_start_hour = self.context.start_hour is not None
        has_end_hour = self.context.end_hour is not None
        if has_start_hour and has_end_hour:
            samehour = self.context.start_hour == self.context.end_hour
            sameday = sameday and samehour
        return sameday

    def iso8601(self, date):
        if date is None:
            return ""
        return date.isoformat()

    def start_iso8601(self):
        return self.iso8601(self.context.start)

    def end_iso8601(self):
        return self.iso8601(self.context.end)

    def localized(self, date=None, time=None):
        if date is not None:
            return date.strftime("%d/%m/%Y")
        if time is not None:
            return time

    def start_date_localized(self):
        return self.localized(date=self.context.start)

    def start_hour_localized(self):
        return self.localized(time=self.context.start_hour)

    def end_date_localized(self):
        return self.localized(date=self.context.end)

    def end_hour_localized(self):
        return self.localized(time=self.context.end_hour)

    def location(self):
        return ""
