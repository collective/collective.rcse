from cioppino.twothumbs import rate
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from cioppino.twothumbs import _


class Like(BrowserView):
    """Like the context"""
    def __call__(self):
        rate.setupAnnotations(self.context)
        action = rate.loveIt(self.context)
        status = IStatusMessage(self.request)
        if action == "like":
            msg = _(u"You liked this. Thanks for the feedback!")
        else:
            msg = _(u"Your vote has been removed.")
        status.add(msg)
        object_url = self.context.absolute_url()
        self.request.response.redirect(object_url)


class DisLike(BrowserView):
    """DisLike the context"""
    def __call__(self):
        rate.setupAnnotations(self.context)
        action = rate.hateIt(self.context)
        status = IStatusMessage(self.request)
        if action == "dislike":
            msg = _(u"You dislike this. Thanks for the feedback!")
        else:
            msg = _(u"Your vote has been removed.")
        status.add(msg)
        object_url = self.context.absolute_url()
        self.request.response.redirect(object_url)
