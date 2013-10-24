from collective.requestaccess.browser.requests import ReviewRequestsView
from collective.rcse.content.group import get_group
from z3c.form.interfaces import HIDDEN_MODE
from collective.requestaccess.manager import RequestManager, ProxyRequest
from plone.uuid.interfaces import IUUID
from collective.requestaccess.interfaces import RequestSchema
from zope import interface
from plone.app.uuid.utils import uuidToObject


class RCSERequestManager(RequestManager):
    """Override the request manager from collective.requestaccess
    to support proxygroup"""

    def update(self):
        RequestManager.update(self)
        self.group = get_group(self.context)
        self.proxy_manager = None
        if self.group is not None:
            name = "@@proxy_group_manager"
            self.proxy_manager = self.group.unrestrictedTraverse(name)
            self.proxy_manager.update()
            self.proxy_group = self.proxy_manager.proxy
            self.group = self.proxy_manager.group

    def get(self, query=None):
        results = RequestManager.get(self, query=query)
        group = get_group(self.context)
        if 'target_path' in query and self.proxy_group is not None and self.proxy_group != self.context:
            proxy_query = {"target_path": '/'.join(self.proxy_group.getPhysicalPath())}
            brains = self.catalog(**proxy_query)
            results.extend(self._get_proxy_from_brain(brains))
        return results
