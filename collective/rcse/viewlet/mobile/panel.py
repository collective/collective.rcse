from zope.viewlet.interfaces import IViewletManager
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPanelLeft(IViewletManager):
    """A viewlet manager that sits on the left panel"""


class IPanelRight(IViewletManager):
    """A viewlet manager that sits on the left panel"""


class AddContent(common.ContentActionsViewlet, common.ContentViewsViewlet):
    """add content"""

    index = ViewPageTemplateFile('templates/addcontent.pt')

    def update(self):
        common.ContentActionsViewlet.update(self)
        common.ContentViewsViewlet.update(self)


class Search(common.ViewletBase):
    index = ViewPageTemplateFile('templates/search.pt')


class Contacts(common.ViewletBase):
    index = ViewPageTemplateFile('templates/contacts.pt')


class Favorites(common.ViewletBase):
    index = ViewPageTemplateFile('templates/favorites.pt')


class Agenda(common.ViewletBase):
    index = ViewPageTemplateFile('templates/agenda.pt')
