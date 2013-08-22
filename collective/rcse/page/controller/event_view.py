import icalendar
from Products.Five.browser import BrowserView
from plone.uuid.interfaces import IUUID
from plone.app.event.dx.behaviors import IEventAccessor
from plone.app.event.browser.event_view import EventView as BaseView
import calendar


class EventView(BaseView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.calendar = {k: v for k,v in enumerate(calendar.month_abbr)}

    def sameday(self):
        if hasattr(self.context, 'whole_day'):
            return self.context.whole_day
        if self.data.end is None:
            return True
        sameday = self.data.start == self.data.end
        return sameday

    def iso8601(self, date):
        if date is None:
            return ""
        return date.isoformat()

    def start_iso8601(self):
        return self.iso8601(self.data.start)

    def end_iso8601(self):
        return self.iso8601(self.data.end)

    def localized(self, date=None, time=None):
        if date is not None:
            return date.strftime("%d/%m/%Y")
        if time is not None:
            return time

    def start_date_localized(self):
        return self.localized(date=self.data.start)

    def end_date_localized(self):
        return self.localized(date=self.data.end)

    def location(self):
        return self.data.location

    def contact_name(self):
        return self.data.contact_name
    
    def contact_email(self):
        return self.data.contact_email
    
    def contact_phone(self):
        return self.data.contact_phone

    def month_name(self, monthint):
        return self.calendar.get(monthint)

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
            self.event.add('dtstart', self.data.start)
            self.event.add('dtend', self.data.end)
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
