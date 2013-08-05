from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID
from Products.ZCatalog.interfaces import ICatalogBrain
from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.rcse.settings import IDocumentActionsIcons


class TimelineItemView(BrowserView):
    """generic view to display an item in the timeline"""

    def __call__(self):
        self.update()
        return self.index()

    def __init__(self, context, request):
        if ICatalogBrain.providedBy(context):
            self.context = context.getObject()
        else:
            self.context = context
        self.request = request
        self.membership = None
        self.portal_url = None
        self.tileid = None
        self.group = None
        self.group_url = None
        self.group_title = None
        self.effective_date = None
        self.creator_info = None
        self.actions = None
        self.actions_icon = None
        self.typesUseViewActionInListings = None

    def update(self):
        if self.membership is None:
            self.membership = getToolByName(self.context, "portal_membership")
        if self.portal_url is None:
            self.portal_url = getToolByName(self.context, 'portal_url')()
        if self.tileid is None:
            self.tileid = IUUID(self.context)
        if self.group is None:
            self.group = self.context.aq_inner.aq_parent
        if self.group_url is None:
            self.group_url = self.group.absolute_url()
        if self.group_title is None:
            self.group_title = self.group.Title()
        if self.effective_date is None:
            self.effective_date = self.get_effective_date()
        if self.creator_info is None:
            name = "@@creator_memberinfo"
            self.creator_info = self.context.restrictedTraverse(name)
        if self.actions is None:
            self.context_state = getMultiAdapter((self.context, self.request),
                                                 name=u'plone_context_state')
            self.actions = self.context_state.actions('document_actions')
        if self.actions_icon is None:
            self._getActionsIcons()
        if self.typesUseViewActionInListings is None:
            pp = getToolByName(self.context, 'portal_properties')
            self.typesUseViewActionInListings = pp.site_properties.getProperty(
                'typesUseViewActionInListings', ()
            )

    def get_content(self):
        return self.context.restrictedTraverse('tile_view')()

    def _getActionsIcons(self):
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

    def get_effective_date(self):
        effective = None
        if self.context.effective_date is not None:
            effective = self.context.effective_date
        elif self.context.modification_date is not None:
            effective = self.context.modification_date
        elif self.context.creation_date is not None:
            effective = self.context.creation_date

        if effective is not None:
            return effective.strftime("%d-%m-%Y")
        return ""
