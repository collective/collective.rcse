from collective.rcse.page.controller.group_base import BaseView


class CalendarView(BaseView):
    """A filterable timeline"""
    filter_type = set("collective.rcse.audio")
