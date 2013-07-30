from collective.rcse.page.controller.group_base import BaseView


class CalendarView(BaseView):
    """A view of events in a calendar"""
    filter_type = ["collective.rcse.event"]
