from zope.viewlet.interfaces import IViewletManager
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPanelLeft(IViewletManager):
    """A viewlet manager that sits on the left panel"""


class IPanelRight(IViewletManager):
    """A viewlet manager that sits on the left panel"""


class AddContent(ViewletBase):
    """add content"""

    index = ViewPageTemplateFile('templates/addcontent.pt')


class Search(ViewletBase):
    index = ViewPageTemplateFile('templates/search.pt')


class Contacts(ViewletBase):
    index = ViewPageTemplateFile('templates/contacts.pt')


class Favorites(ViewletBase):
    index = ViewPageTemplateFile('templates/favorites.pt')


class Agenda(ViewletBase):
    index = ViewPageTemplateFile('templates/agenda.pt')
