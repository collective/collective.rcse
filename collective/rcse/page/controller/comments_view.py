import sys

from plone.app.discussion.browser import comments as base
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.uuid.utils import uuidToObject
from plone.memoize.view import memoize
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope import interface
from zope.component._api import getUtility
from zope.browsermenu.interfaces import IBrowserMenu


def should_display_comments(context, request):
    """Return True if comments on this context should be displayed"""
    if context.portal_type == "collective.rcse.discussion":
        return True
    should_display_comments = False
#     displayed = request.displayeds.get("DISPLAY_COMMENTS", "")
    sdm = context.session_data_manager
    session = sdm.getSessionData(create=True)
    displayed = session.get("DISPLAY_COMMENTS", "")
    if displayed:
        context_path = "/".join(context.getPhysicalPath())
        should_display_comments = context_path in displayed
    return should_display_comments


def must_display_comments(context, request):
    """Mark this context to ask to display comments"""
    if context.portal_type == "collective.rcse.discussion":
        return
    context_path = '/'.join(context.getPhysicalPath())
#    displayed = request.cookies.get("DISPLAY_COMMENTS", "")
    sdm = context.session_data_manager
    session = sdm.getSessionData(create=True)
    displayed = session.get("DISPLAY_COMMENTS", "")
    paths = displayed.split(";")
    if context_path not in paths:
        paths.append(context_path)
        displayed = ";".join(paths)
        remove = 1
        while sys.getsizeof(displayed) > 3999:
            displayed = ";".join(paths[remove:])
            remove += 1
        #request.response.setCookie("DISPLAY_COMMENTS", displayed)
        session.set("DISPLAY_COMMENTS", displayed)


def dont_display_comments(context, request):
    if context.portal_type == "collective.rcse.discussion":
        return
    context_path = '/'.join(context.getPhysicalPath())
    #displayed = request.cookies.get("DISPLAY_COMMENTS", "")
    sdm = context.session_data_manager
    session = sdm.getSessionData(create=True)
    displayed = session.get("DISPLAY_COMMENTS", "")
    paths = displayed.split(";")
    if context_path in paths:
        paths.remove(context_path)
        displayed = ";".join(paths)
        #request.response.setCookie("DISPLAY_COMMENTS", displayed)
        session.set("DISPLAY_COMMENTS", displayed)


class ICommentsView(interface.Interface):
    """allowed_interface"""
    def __call__():
        """Return the rendered content"""
    def render_viewlet():
        """return the rendered content of the corresponding viewlet"""


def get_comments_context(context, request):
    context_uuid = IUUID(context, None)
    uid = request.get("uid", None)
    if IPloneSiteRoot.providedBy(context):
        if uid is None:
            raise ValueError()
    if INavigationRoot.providedBy(context):
        if uid is not None and uid != str(context_uuid):
            context = uuidToObject(uid)
        if not context:
            raise ValueError()
    return context


class CommentsView(base.CommentsViewlet):
    """revamp this in a view"""
    interface.implements(ICommentsView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.context = get_comments_context(self.context, self.request)
        base.CommentsViewlet.update(self)
        self.form.widgets['text'].id = None
        self.form.widgets['text'].update()
        self.getMenuForReplies()

    def getMenuForReplies(self):
        self.menu = {}
        if self.get_replies() is None:
            return
        for reply in list(self.get_replies()):
            self.menu[reply['id']] = getUtility(
                IBrowserMenu,
                name='plone_contentmenu_workflow'
            ).getMenuItems(reply['comment'], self.request)
            if len(self.menu[reply['id']]):
                del self.menu[reply['id']][-1]

    @memoize
    def how_many(self):
        replies = self.get_replies()
        if replies:
            return len(list(replies))
        return 0

    def uid(self):
        return IUUID(self.context, None)
