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
            self.event.add('dtstart', )
            self.eventadd('summary', 'Python meeting about calendaring')
            self.eventadd('dtstart', self.context.start)
            self.eventadd('dtend', self.context.end)
            self.event['uid'] = IUUID(self.context)
            self.eventadd('priority', 5)
        if self.cal is None:
            self.cal = icalendar.Calendar()
            self.cal.add_component(self.event)

    def index(self):
        return self.cal.to_ical()
