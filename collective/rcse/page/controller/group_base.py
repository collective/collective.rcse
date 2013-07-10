from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope import interface
from zope import schema
from Products.CMFCore.interfaces._tools import ICatalogTool


class IBaseView(interface.Interface):
    """Base view for group, has builtin feature like filter"""

    filter_type = schema.ASCIILine(title=u"Filter on portal_type")
    query = schema.Dict(title=u"query for the catalog")
    catalog = schema.Object(title=u"Portal catalog",
                            schema=ICatalogTool)

    def get_items():
        """return catalog query results"""


class BaseView(BrowserView):
    """make a dashboard view which is responsive"""
    interface.implements(IBaseView)

    filter_type = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.query = {}

        self.catalog = None
        self.portal_state = None
        self.context_state = None
        self.authenticated_member = None

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        if self.catalog is None:
            self.catalog = getToolByName(self.context, "portal_catalog")
        self._update_query()

    def _update_query(self):
        """build query from request"""
        # look at @@search code view
        if self.filter_type is not None:
            self.query["portal_type"] = self.filter_type

    def get_items(self):
        return self.catalog(**self.query)
