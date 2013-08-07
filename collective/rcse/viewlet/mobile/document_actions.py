from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets.content import DocumentActionsViewlet
from plone.app.layout.viewlets.common import ViewletBase


class DocumentIconActionsViewlet(DocumentActionsViewlet):
    """We replace action by icons if it is set in the registry.
    All actions without icon are put in a popup provided by a [+] icon."""

    def update(self):
        super(DocumentIconActionsViewlet, self).update()
        self.actions_icon = []
        for action in self.actions:
            if action['icon']:
                self.actions_icon.append(action)
        for action in self.actions_icon:
            self.actions.remove(action)
