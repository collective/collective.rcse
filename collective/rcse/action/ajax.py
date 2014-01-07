import json

from Acquisition import aq_inner, aq_parent
from plone.app.discussion.browser.moderation import DeleteComment
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.i18n import translate
from zope import component

from collective.watcherlist.interfaces import IWatcherList
from collective.favoriting.browser import favoriting_view
from collective.rcse.action import cioppino_twothumbs
from collective.rcse.page.controller import comments_view
from collective.whathappened.browser import subscribe
from collective.rcse.action import watchers


class AjaxAction(BrowserView):
    """Make an action url handle ajax request
    Process
    * js: InitAjaxAction
      [resources/dev/js/themedesktop.js]
     make link of actions behing ajax throw this base action. Assure ajax_load
     is here, using data:{ajax_load:true} or adding an input name="ajax_load"
     to the form

    * user: click an ajax action

    * server: this current base view do the following:
      - detect if this is an ajax action (using ajax_load from request)
      - execute the action
      - if it's ajax -> block redirect, render
        '@@plone.abovecontenttitle.documentactions'
      - return the rendered content with messages in json
    """
    action_class = None

    def do_action(self):
        if self.action_class is not None:
            action = self.action_class(self.context, self.request)
        else:
            action = self.action
        return action()

    def update_request(self):
        response = self.request.response
        if response.status in (301, 302):
            response.setStatus(200)
        response.setHeader("Content-type", "application/json")

    def get_context(self):
        return self.context

    def ajax_return(self):
        #remove status message ...
        data = {}
        data['messages'] = []
        #the context may have change (for example: plone.comments)
        context = self.get_context()
        name = 'plone.abovecontenttitle.documentactions'
        html = context.restrictedTraverse(name)()
        data['document-actions-wrapper'] = html
        messages = IStatusMessage(self.request).show()
        for message in messages:
            body = translate(message.message, context=self.request)
            data['messages'].append({'message': body,
                                     'type': message.type})
        return json.dumps(data)

    def __call__(self):
        ajax = self.request.get('ajax_load', False)
        original_result = self.do_action()
        if not ajax:
            return original_result

        self.update_request()
        return self.ajax_return()

    def action(self):
        raise NotImplementedError()


class FavoritingAdd(AjaxAction):
    action_class = favoriting_view.Add


class FavoritingRm(AjaxAction):
    action_class = favoriting_view.Rm


class Like(AjaxAction):
    action_class = cioppino_twothumbs.Like


class DisLike(AjaxAction):
    action_class = cioppino_twothumbs.DisLike


class Subscribe(AjaxAction, subscribe.Subscribe):
    action_class = subscribe.Subscribe

    def __init__(self, context, request):
        subscribe.Subscribe.__init__(self, context, request)
        AjaxAction.__init__(self, context, request)

    def __call__(self):
        self.update()
        return AjaxAction.__call__(self)

    def _hasParentSubscription(self, path):
        if self.context.portal_type == 'collective.rcse.group':
            return False
        path = path.rpartition('/')[0]
        context = aq_parent(self.context)
        while len(path) > 0 and path != '/':
            if '/' not in path:
                break
            subscription = self.storage.getSubscription(path)
            if subscription is not None and subscription.wants:
                return True
            if context.portal_type == 'collective.rcse.group':
                break
            path = path.rpartition('/')[0]
            context = aq_parent(context)
        return False


class Unsubscribe(Subscribe):
    action_class = subscribe.Unsubscribe


class Blacklist(Subscribe):
    action_class = subscribe.Blacklist


class Unblacklist(Subscribe):
    action_class = subscribe.Unblacklist


class ToggleDisplayInMyNews(AjaxAction):
    action_class = watchers.ToggleDisplayInMyNews

    def __init__(self, context, request):
        super(ToggleDisplayInMyNews, self).__init__(context, request)
        self.watchers = None

    def update(self):
        if self.watchers is None:
            context = aq_inner(self.context)
            self.watchers = component.queryAdapter(
                context,
                interface=IWatcherList,
                name="group_watchers",
                default=None
            )

    def is_watching(self):
        self.update()
        if self.watchers is None:
            return False
        return self.watchers.isWatching()


class TriggerDisplayComments(AjaxAction):

    def action(self):
        if comments_view.should_display_comments(self.context, self.request):
            comments_view.dont_display_comments(self.context, self.request)
        else:
            comments_view.must_display_comments(self.context, self.request)
        referer = self.request.get("HTTP_REFERER")
        if not referer:
            referer = self.context.absolute_url()
        self.request.response.redirect(referer)
        return u""


class Comments(AjaxAction):
    """name="plone.comments.ajax"
    it is a quite differnet use case because the update do the action.
    """
    action_class = comments_view.CommentsView

    def __call__(self):
        #because the rendering of document_actions will execute the form...
        ajax = self.request.get('ajax_load', False)
        if not ajax:
            return self.do_action()
        data = self.ajax_return()
        self.update_request()
        return data

    def get_context(self):
        return comments_view.get_comments_context(self.context, self.request)


class DeleteCommentAction(AjaxAction):
    action_class = DeleteComment

    def get_context(self):
        comment = aq_inner(self.context)
        conversation = aq_parent(comment)
        content_object = aq_parent(conversation)
        return content_object
