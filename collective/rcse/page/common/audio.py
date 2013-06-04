from collective.mediaelementjs.browser.view import File as MediaElementJS


class AudioView(MediaElementJS):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self._audio = {}
        context_url = self.context.absolute_url()
        filename = self.context.file.filename.encode('utf-8')
        mimetype = self.context.file.contentType
        source = {}
        source["src"] = context_url + '/@@download/file/' + filename
        source["mimetype"] = mimetype
        source["duration"] = ""
        self.source = source

    def href(self):
        return self.source["src"]

    def audio(self):
        return self.source

    def getFilename(self):
        return self.context.file.filename.encode('utf-8')

    def getContentType(self):
        return self.context.file.contentType
