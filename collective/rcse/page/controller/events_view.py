import calendar

from plone.app.event.base import localized_today, construct_calendar
from Products.CMFPlone.utils import getToolByName
from zope.i18nmessageid import MessageFactory

from collective.rcse.page.controller.group_base import BaseView
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView


PLMF = MessageFactory('plonelocales')


class EventsView(BaseView):
    """A view of events in a calendar"""
    filter_type = ["collective.rcse.event"]


class NavigationRootEventsView(EventsView, NavigationRootBaseView):
    def update(self):
        EventsView.update(self)
        NavigationRootBaseView.update(self)
