from zope import interface
from plone.app.discussion.browser import comments as base
from plone.uuid.interfaces import IUUID
import sys
import logging
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.uuid.utils import uuidToURL, uuidToObject
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
logger = logging.getLogger("collective.rcse")


def should_display_comments(context, request):
    """Return True if comments on this context should be displayed"""
    should_display_comments = False
#     displayed = request.displayeds.get("DISPLAY_COMMENTS", "")
    sdm = context.session_data_manager
    session = sdm.getSessionData(create=True)
    displayed = session.get("DISPLAY_COMMENTS", "")
    if displayed:
        paths = displayed.split(';')
        context_path = "/".join(context.getPhysicalPath())
        should_display_comments = context_path in displayed
    logger.info("should_display_comments: %s" % should_display_comments)
    return should_display_comments


def must_display_comments(context, request):
    """Mark this context to ask to display comments"""
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
            remove +=1
        #request.response.setCookie("DISPLAY_COMMENTS", displayed)
        session.set("DISPLAY_COMMENTS", displayed)
        logger.info("must_display_comments")


def dont_display_comments(context, request):
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
        logger.info("dont_display_comments")


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
    import logging; logging.getLogger("log").info(context.absolute_url())
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
