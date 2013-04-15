from zope.viewlet.interfaces import IViewletManager
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IFooter(IViewletManager):
    """A viewlet manager that sits on the left panel"""

