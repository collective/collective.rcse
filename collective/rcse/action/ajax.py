import json
from Acquisition import aq_inner, aq_parent
from Products.Five.browser import BrowserView
from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.interfaces import IStatusMessage
from Products.statusmessages.adapter import _decodeCookieValue
from plone.uuid.interfaces import IUUID
from collective.favoriting.browser import favoriting_view
from zope.annotation.interfaces import IAnnotations
from collective.rcse.action import cioppino_twothumbs
from zope.i18n import translate
from collective.rcse.page.controller import comments_view
from plone.app.discussion.browser.moderation import DeleteComment


class AjaxAction(BrowserView):
    """Make an action url handle ajax request
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
        ajax = self.request.get('ajax', False)
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
    action_class = comments_view.CommentsView

    def __call__(self):
        #because the rendering of document_actions will execute the form...
        ajax = self.request.get('ajax', False)
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
