from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets.content import DocumentActionsViewlet
from plone.app.layout.viewlets.common import ViewletBase

from collective.rcse.settings import IDocumentActionsIcons


class DocumentIconActionsViewlet(DocumentActionsViewlet):
    """We replace action by icons if it is set in the registry.
    All actions without icon are put in a popup provided by a [+] icon."""

    def update(self):
        ViewletBase.update(self)
        super(DocumentIconActionsViewlet, self).update()
        reg = getUtility(IRegistry)
        config = reg.forInterface(IDocumentActionsIcons, False)
        if not config or not hasattr(config, 'mapping'):
            return
        self.mapping = config.mapping
        self.actions_icon = []
        for action in self.actions:
            if action['id'] in self.mapping.keys():
                action = action
                action['icon'] = self.mapping[action['id']]
                self.actions_icon.append(action)
        for action in self.actions_icon:
            self.actions.remove(action)
