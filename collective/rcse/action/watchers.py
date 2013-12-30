from Acquisition import aq_inner
from collective.rcse.content.group import get_group
from collective.rcse import i18n
from collective.watcherlist.interfaces import IWatcherList
from plone.indexer import indexer
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope import interface
from zope import component
from dexterity.membrane.membrane_helpers import get_membrane_user
from logging import getLogger

logger = getLogger(__name__)

"""
The global process of this is quite simple:
* You register yourself as watcher of a group
* Every content added/modified in that group will have watchers synchronized
* So to build 'My news' you just have to list every content where you are
  a watcher
"""


class IDisplayInMyNewsHelper(interface.Interface):
    """controller of the action"""
    def toggle_watching():
        """activate/desactivate watching of the current user on the current
        context"""
    def is_watching():
        """Return True if the current user is watching the context.
        Else, return False"""


class ToggleDisplayInMyNews(BrowserView):
    """Add the current user as watcher of the current group."""
    interface.implements(IDisplayInMyNewsHelper)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.member = None
        self.catalog = None
        self.watchers = None

    def __call__(self):
        self.update()
        self.toggle_watching()
        if self.is_watching():
            msg = i18n.msg_watchers_add
        else:
            msg = i18n.msg_watchers_rm
        IStatusMessage(self.request).add(msg)
        self.request.response.redirect(self.nextURL())

    def nextURL(self):
        referer = self.request.get("HTTP_REFERER", None)
        if not referer:
            referer = self.context.absolute_url()
        return referer

    def update(self):
        if self.member is None:
            memship = getToolByName(self.context, 'portal_membership', None)
            if memship is not None:
                self.member = memship.getAuthenticatedMember()
        if self.watchers is None:
            context = aq_inner(self.context)
            self.watchers = component.queryAdapter(
                context,
                interface=IWatcherList,
                name="group_watchers",
                default=None
            )
        if self.catalog is None:
            self.catalog = getToolByName(self.context, "portal_catalog")

    def toggle_watching(self):
        self.watchers.toggle_watching()
        self.context.reindexObject()
        self.reindex_last_items()

    def reindex_last_items(self):
        self.context.reindexObject(idxs=["group_watchers"])
        query = {}
        query["path"] = {
            "query": "/".join(self.context.getPhysicalPath()),
            "depth": 1,
        }
        query["sort_on"] = "modified"
        query["sort_order"] = "reverse"
        query["sort_limit"] = 5
        brains = self.catalog(**query)
        for brain in brains:
            brain.getObject().reindexObject(idxs=["group_watchers"])

    def is_watching(self):
        self.update()
        if self.watchers is None:
            return False
        return self.watchers.isWatching()


def get_followers(context):
    """Return people who follow the first creator"""
    creator, watcherlist = _getWatcherList(context)
    if watcherlist:
        msg = "watchers of %s: %s" % (creator, watcherlist.watchers)
        logger.debug(msg)
        return watcherlist.watchers
    return []


def _getWatcherList(context):
    creator = None
    membrane = None
    if context.portal_type == "collective.rcse.member":
        membrane = context
        try:
            creator = context.creators[0]
        except IndexError:
            logger.debug("%s has no creator" % context.absolute_url())
    else:
        if hasattr(context, 'creators'):
            try:
                creator = context.creators[0]
            except IndexError:
                logger.debug("%s has no creator" % context.absolute_url())
        elif hasattr(context, 'Creators'):
            try:
                creator = context.Creators()[0]
            except IndexError:
                logger.debug("%s has no creator" % context.absolute_url())
        if not creator:
            return (None, [])
        membrane = get_membrane_user(
            context, creator,
            member_type='collective.rcse.member',
            get_object=True
        )
    watcherlist = component.queryAdapter(
        membrane, interface=IWatcherList, name="group_watchers", default=None
    )
    return (creator, watcherlist)


@indexer(interface.Interface)
def get_group_watchers(context):
    """Index people who should have context appear in their timeline."""
    if context.portal_type in (
        "Discussion Item",
        "collective.history.useraction"
    ):
        return
    watchers = []
    context = aq_inner(context)
    group = context
    #Add content's creators as watchers
    if hasattr(context, 'creators'):
        watchers.extend(context.creators)
    elif hasattr(context, 'Creators'):
        watchers.extend(context.Creators())
    #Add followers of the first content's creator as watchers
    watchers.extend(get_followers(context))
    if context.portal_type != "collective.rcse.group":
        group = get_group(context)
        if group and hasattr(group, 'creators'):
            watchers.extend(group.creators)
    #Add watchers of the group as watchers of the content
    watcherlist = component.queryAdapter(
        group, interface=IWatcherList, name="group_watchers", default=None
    )
    if watcherlist:
        watchers.extend(watcherlist.watchers)
    watchers = tuple(set(watchers))
    return watchers
