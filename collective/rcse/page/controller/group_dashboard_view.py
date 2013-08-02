from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser import BrowserView
from zope import interface


class IDashboardPortletManager(IPortletManager, IColumn):
    """Marker interface for portlet manager"""


class DashboardView(BrowserView):
    """make a dashboard view which is responsive"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        pass

    def canManagePortlets(self):
        mt = getToolByName(self.context, 'portal_membership')
        return mt.checkPermission('Modify Portal Content', self.context)
