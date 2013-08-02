from plone.app.portlets.browser.editmanager import EditPortletManagerRenderer
from zope import interface

from collective.rcse.portlets.interfaces import IManageDashboardView


class DashboardGroupEditPortletManagerRenderer(EditPortletManagerRenderer):
    adapts(interface.Interface, IDefaultBrowserLayer,
           IManageDashboardView, )
