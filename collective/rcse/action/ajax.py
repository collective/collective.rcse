import json
from Products.Five.browser import BrowserView
from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.interfaces import IStatusMessage
from Products.statusmessages.adapter import _decodeCookieValue
from plone.uuid.interfaces import IUUID
from collective.favoriting.browser import favoriting_view
from zope.annotation.interfaces import IAnnotations
from collective.rcse.action import cioppino_twothumbs
from zope.i18n import translate


class AjaxAction(BrowserView):
    """Make an action url handle ajax request
    """
    action_class = None

    def __call__(self):
        ajax = self.request.get('ajax', False)
        response = self.request.response
        action = self.action_class(self.context, self.request)
        original_result = action()
        if not ajax:
            return original_result

        if response.status in (301, 302):
            response.setStatus(200)
        response.setHeader("Content-type", "application/json")
        #remove status message ...
        messages = IStatusMessage(self.request).show()
        data = {}
        data['messages'] = []
        data['uid'] = IUUID(self.context)
        data['document-actions-wrapper'] = self.context.restrictedTraverse('plone.abovecontenttitle.documentactions')()
        for message in messages:
            body = translate(message.message, context=self.request)
            data['messages'].append({'message': body,
                                     'type': message.type})
        return json.dumps(data)


class FavoritingAdd(AjaxAction):
    action_class = favoriting_view.Add


class FavoritingRm(AjaxAction):
    action_class = favoriting_view.Rm


class Like(AjaxAction):
    action_class = cioppino_twothumbs.Like


class DisLike(AjaxAction):
    action_class = cioppino_twothumbs.DisLike
