from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from Products.Five.browser import BrowserView


class AudioSchema(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    file = NamedBlobFile(title=u"Audio file")


class AudioView(BrowserView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.sources = []
        context_url = self.context.absolute_url()
        filename = self.context.file.filename.encode('utf-8')
        mimetype = self.context.file.contentType
        source = {}
        source["src"] = context_url + '/@@download/file/' + filename
        source["mimetype"] = mimetype
        self.sources.append(source)

    def get_sources(self):
        """
        file   mimetype
        MP3    audio/mpeg
        Ogg    audio/ogg
        Wav    audio/wav"""
        return self.sources
