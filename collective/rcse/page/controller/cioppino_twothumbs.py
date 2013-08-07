from cioppino.twothumbs import rate
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from cioppino.twothumbs import _


class Base(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.statusmessage = None
        self.message = None

    def update(self):
        rate.setupAnnotations(self.context)
        if self.statusmessage is None:
            self.statusmessage = IStatusMessage(self.request)

    def __call__(self):
        self.update()
        self.doIt()
        self.statusmessage.add(self.message)
        self.request.response.redirect(self.nextURL())

    def nextURL(self):
        referer = self.request.get("HTTP_REFERER", None)
        if not referer:
            referer = self.context.absolute_url()
        return referer


class Like(Base):
    """Like the context"""
    def doIt(self):
        action = rate.loveIt(self.context)
        if action == "like":
            self.message = _(u"You liked this. Thanks for the feedback!")
        else:
            self.message = _(u"Your vote has been removed.")


class DisLike(Base):
    """DisLike the context"""
    def doIt(self):
        action = rate.hateIt(self.context)
        if action == "dislike":
            self.message = _(u"You dislike this. Thanks for the feedback!")
        else:
            self.message = _(u"Your vote has been removed.")


class IsLikedByMe(Base):
    def __call__(self):
        self.update()
        myvote = rate.getMyVote(self.context)
        return myvote == 1


class IsDisLikedByMe(Base):
    def __call__(self):
        self.update()
        myvote = rate.getMyVote(self.context)
        return myvote == -1
