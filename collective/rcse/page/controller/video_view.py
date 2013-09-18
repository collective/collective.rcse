from plone.directives import form
from plone.namedfile.field import NamedBlobFile

from collective.transcode.star.browser.viewlets import TranscodeViewlet
from collective.transcode.star.interfaces import ITranscoded
from collective.rcse.i18n import RCSEMessageFactory


_ = RCSEMessageFactory


class VideoView(TranscodeViewlet):
    """default view"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        return self.index()

    def isTranscoded(self):
        return ITranscoded.providedBy(self.context)
