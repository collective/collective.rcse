import json

from Products.Five.browser import BrowserView
from zope.i18n import translate

from collective.whathappened.browser.notifications import getHotNotifications
from collective.whathappened.browser.notifications import getUnseenCount


class NotificationAjax(BrowserView):
    def updateResponse(self):
        response = self.request.response
        if response.status in (301, 302):
            response.setStatus(200)
        response.setHeader("Content-type", "application/json")

    def __call__(self):
        self.updateResponse()
        notifications = getHotNotifications(self.context, self.request)
        for notification in notifications:
            notification['title'] = translate(
                notification['title'],
                context=self.request
                )
        unseenCount = getUnseenCount(self.context, self.request)
        return json.dumps({'unseenCount': unseenCount,
                           'notifications': notifications})
