from plone.directives import form
from plone.namedfile.field import NamedBlobFile

from collective.mediaelementjs.dexterity import MediaElementJSFileView

from collective.rcse.i18n import RCSEMessageFactory


_ = RCSEMessageFactory


class VideoSchema(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    file = NamedBlobFile(title=_(u"Video file"))


class VideoView(MediaElementJSFileView):
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
