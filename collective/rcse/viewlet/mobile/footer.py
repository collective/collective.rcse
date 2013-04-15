from zope.viewlet.interfaces import IViewletManager
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IFooter(IViewletManager):
    """A viewlet manager that sits on the left panel"""


class Links(ViewletBase):
    index = ViewPageTemplateFile('templates/links.pt')

    def themeswitcher_desktop_url(self):
        #update the cookie to switch to desktop version
        url_suffix = "/@@themeswitcher_cookie?theme=collective.rcse.desktop"
        return self.site_url + url_suffix
