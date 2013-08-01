import calendar

from plone.app.event.base import localized_today, construct_calendar
from Products.CMFPlone.utils import getToolByName
from zope.i18nmessageid import MessageFactory

from collective.rcse.page.controller.group_base import BaseView

PLMF = MessageFactory('plonelocales')


class CalendarView(BaseView):
    """A view of events in a calendar"""
    filter_type = ["collective.rcse.event"]

    def __init__(self, context, request):
        super(CalendarView, self).__init__(context, request)
        self.events = None

    def update(self):
        super(CalendarView, self).update()
        if self.events is None:
            self.events = self.get_month_events()

    def _initializeDate(self):
        ts = getToolByName(self.context, 'translation_service')

        self.today = localized_today(self.context)
        self.year = int(self.request.get('year', self.today.year))
        self.month = int(self.request.get('month', self.today.month))
        self.month_name = PLMF(ts.month_msgid(self.month),
                               default=ts.month_english(self.month))

        cal = calendar.Calendar()
        monthdays = cal.itermonthdates(self.year, self.month)
        self.monthdays = [day for day in monthdays]
        self.weekdays = []
        for day in cal.iterweekdays():
            weekday = PLMF(ts.day_msgid((day + 1) % 7),
                           default=ts.weekday_english(day))
            self.weekdays.append(weekday)

    def _setLinks(self):
        url = self.context.absolute_url()
        url_string = '%s/calendar_view?year=%d&month=%d'
        month = self.month == 1 and 12 or self.month - 1
        year = self.month == 1 and self.year - 1 or self.year
        self.prev_month = url_string % (url, year, month)
        month = self.month == 12 and 1 or self.month + 1
        year = self.month == 12 and self.year + 1 or self.year
        self.next_month = url_string % (url, year, month)

    def _update_events_query(self):
        self.start = self.monthdays[0]
        self.end = self.monthdays[-1]
        self.query['end'] = {'query': self.start, 'range': 'min'}
        self.query['start'] = {'query': self.end, 'range': 'max'}
        self.query['sort_on'] = 'start'
        del self.query['sort_order']

    def get_month_events(self):
        self._initializeDate()
        self._setLinks()
        self._update_events_query()
        events = self.get_content(batch=False, object=True)
        cal_events = construct_calendar(events, self.start, self.end)
        caldata = [[]]
        for dat in self.monthdays:
            if len(caldata[-1]) == 7:
                caldata.append([])

            date_events = None
            isodat = dat.isoformat()
            if isodat in cal_events:
                date_events = cal_events[isodat]

            caldata[-1].append({'date': dat,
                 'day': dat.day,
                 'prev_month': dat.month < self.month,
                 'next_month': dat.month > self.month,
                 'today': dat.year == self.today.year and\
                          dat.month == self.today.month and\
                          dat.day == self.today.day,
                 'date_string': u"%s-%s-%s" % (dat.year, dat.month, dat.day),
                 'events': date_events})
        self.caldata = caldata
        return events
