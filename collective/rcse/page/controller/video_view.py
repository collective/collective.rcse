from plone.directives import form
from plone.namedfile.field import NamedBlobFile

from collective.mediaelementjs.dexterity import MediaElementJSFileView
from collective.mediaelementjs import metadata_extraction as meta

from collective.rcse.i18n import RCSEMessageFactory


_ = RCSEMessageFactory


class VideoView(MediaElementJSFileView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def _get_metadata(self):
        handle = self.context.file.open()
        metadata = meta.parse_raw(handle)
        handle.close()
        self.source["width"] = meta.defensive_get(metadata, 'width')
        self.source["height"] = meta.defensive_get(metadata, 'height')
        self.source["duration"] = meta.defensive_get(metadata, 'duration')

    def update(self):
        context_url = self.context.absolute_url()
        filename = self.context.file.filename.encode('utf-8')
        mimetype = self.context.file.contentType
        source = {}
        source["src"] = context_url + '/@@download/file/' + filename
        source["mimetype"] = mimetype
        self.source = source
        self._get_metadata()

    def href(self):
        return self.source["src"]

    def video(self):
        return self.source

    def getContentType(self):
        return self.context.file.contentType
