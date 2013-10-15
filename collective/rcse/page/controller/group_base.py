from zope import interface
from zope import schema
from z3c.form import form

from Products.CMFCore.interfaces._tools import ICatalogTool
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from plone.supermodel import model

from plone.autoform.form import AutoExtensibleForm
from plone.app.search.browser import quote_chars
from plone.app.uuid.utils import uuidToObject
from plone.dexterity import utils
from plone.z3cform.layout import FormWrapper

from collective.rcse.i18n import _


class IBaseView(interface.Interface):
    """Base view for group, has builtin feature like filter"""

    filter_type = schema.ASCIILine(title=u"Filter on portal_type")
    query = schema.Dict(title=u"query for the catalog")
    catalog = schema.Object(title=u"Portal catalog",
                            schema=ICatalogTool)

    def get_items():
        """return catalog query results"""


class BaseView(BrowserView):
    """Base view for other group views.
    Filter based on GET parameters and filter_type."""
    interface.implements(IBaseView)

    filter_type = None
    valid_keys = ('sort_on', 'sort_order', 'sort_limit')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.query = {}

        self.catalog = None
        self.portal_state = None
        self.context_path = None
        self.context_state = None
        self.authenticated_member = None

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        if self.catalog is None:
            self.catalog = getToolByName(self.context, "portal_catalog")
        if self.context_path is None:
            self.context_path = '/'.join(self.context.getPhysicalPath())
        self._update_query()

    def _update_query(self):
        """build query from request"""
        self.query = {
            #"path": {'query': self.context_path, 'depth': 1},
            "path": self.context_path,
            "sort_on": "modified",
            "sort_order": "reverse",
#            "sort_limit": 20,
            }
        self._update_query_portal_type()
        text = self.request.get('SearchableText', None)
        if text is not None:
            self.query["SearchableText"] = quote_chars(text)
        for k, v in self.request.form.items():
            if v and k in self.valid_keys:
                self.query[k] = v
        if self.query['sort_on'] == 'relevance':
            del self.query['sort_on']

    def _update_query_portal_type(self):
        types = self.request.get('portal_type', None)
        if types is not None and len(types) > 0:
            self.query["portal_type"] = set(types.split(','))
        if self.filter_type is not None and len(self.filter_type) > 0:
            if self.query.get('portal_type'):
                portal_type = self.query["portal_type"] & set(self.filter_type)
                self.query["portal_type"] = portal_type
            else:
                self.query["portal_type"] = self.filter_type
        if self.query.get("portal_type"):
            self.query["portal_type"] = list(self.query["portal_type"])

    def get_content(self, batch=True, b_size=10, b_start=0, pagerange=7,
                    full=False):
        results = self.catalog(self.query)
        if batch:
            results = Batch(results, int(b_size), int(b_start))#, pagerange=pagerange)
        if full:
            results = [brain.getObject() for brain in results]
        return results


class BaseAddFormSchema(model.Schema):
    where = schema.Choice(
        title=u"Where",
        vocabulary="collective.rcse.vocabulary.groups"
    )


class BaseAddForm(AutoExtensibleForm, form.Form):
#    schema = AddFormSchema
    enableCSRFProtection = True
    msg_added = _(u"Content Added")
    CONTENT_TYPE = ""

#    @button.buttonAndHandler(_(u"Add Image"))
    def handleAdd(self, action, referer=True):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            self.errors = errors
            return
        if self.request.response.getStatus() not in (302, 303):
            self.doAdd(data, referer)

    def doAdd(self, data, referer):
        container = uuidToObject(data['where'])
        item = utils.createContentInContainer(
            container,
            self.CONTENT_TYPE,
            checkConstraints=True,
            **data)

        IStatusMessage(self.request).add(self.msg_added)
        referer_url = self.request.get("HTTP_REFERER")
        if not referer_url:
            referer_url = item.absolute_url()
        if referer:
            self.request.response.redirect(referer_url)
        else:
            self.request.response.redirect(item.absolute_url())


class BaseAddFormView(BaseView, FormWrapper):
    """A filterable timeline"""
    portlets_show = {
        'plone.leftcolumn': True,
        'plone.rightcolumn': False,
        }
#    filter_type = [CONTENT_TYPE]
#    form = AddForm

    def __init__(self, context, request):
        BaseView.__init__(self, context, request)
        FormWrapper.__init__(self, context, request)

    def update(self):
        BaseView.update(self)
        FormWrapper.update(self)
