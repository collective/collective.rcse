import icalendar
from Products.Five.browser import BrowserView
from plone.uuid.interfaces import IUUID


class EventView(BrowserView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        pass

    def sameday(self):
        if hasattr(self.context, 'whole_day'):
            return self.context.whole_day
        if self.context.end is None:
            return True
        sameday = self.context.start == self.context.end
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

    def end_date_localized(self):
        return self.localized(date=self.context.end)

    def location(self):
        return ""


PRODID = "-//Plone.org//NONSGML collective.rcse//EN"
VERSION = "2.0"


class ICSEventView(EventView):
    def __init__(self, context, request):
        EventView.__init__(self, context, request)
        self.event = None
        self.cal = None

    def update(self):
        if self.event is None:
            self.event = icalendar.Event()
            self.event.add('summary', self.context.Description())
            self.event.add('dtstart', self.context.start)
            self.event.add('dtend', self.context.end)
            self.event['uid'] = IUUID(self.context)
            self.event.add('priority', 5)
        if self.cal is None:
            self.cal = icalendar.Calendar()
            self.cal.add_component(self.event)

    def index(self):
        self.request.response.setHeader(
            "Content-Disposition",
            "attachment; filename=%s.ics" % (self.context.getId())
        )
        self.request.response.setHeader(
            "Content-type",
            "text/calendar"
        )
        return self.cal.to_ical()
