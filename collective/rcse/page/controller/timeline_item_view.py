from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID
from Products.ZCatalog.interfaces import ICatalogBrain
from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from cioppino.twothumbs import rate
from collective.favoriting.browser.favoriting_view import VIEW_NAME
from collective.rcse import icons
from collective.rcse.content.group import get_group


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
        self.rate = None
        self.fav = None

    def update(self):
        if self.membership is None:
            self.membership = getToolByName(self.context, "portal_membership")
        if self.portal_url is None:
            self.portal_url = getToolByName(self.context, 'portal_url')()
        if self.tileid is None:
            self.tileid = IUUID(self.context)
        if self.group is None:
            self.group = get_group(self.context)
        if self.group_url is None:
            self.group_url = self.group.absolute_url()
        if self.group_title is None:
            self.group_title = self.group.Title()
        if self.effective_date is None:
            self.effective_date = self.get_effective_date()
        if self.creator_info is None:
            name = "@@creator_memberinfo"
            self.creator_info = self.context.restrictedTraverse(name)
        if self.typesUseViewActionInListings is None:
            pp = getToolByName(self.context, 'portal_properties')
            self.typesUseViewActionInListings = pp.site_properties.getProperty(
                'typesUseViewActionInListings', ()
            )
        if self.rate is None:
            self.rate = rate.getTally(self.context)
        if self.fav is None:
            self.fav = self.context.restrictedTraverse(VIEW_NAME)
        self.icon = icons.get(self.context.portal_type)

    def get_content(self):
        return self.context.restrictedTraverse('tile_view')()

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

    def get_how_many_like(self):
        return self.rate["ups"]

    def is_liked_by_be(self):
        return self.rate["mine"] == 1

    def get_how_many_dislike(self):
        return self.rate["downs"]

    def is_disliked_by_be(self):
        return self.rate["mine"] == -1

    def get_how_many_star(self):
        return self.fav.how_many()
