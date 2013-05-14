from plone.directives import form
from plone.namedfile.field import NamedBlobFile
#from Products.Five.browser import BrowserView
from collective.rcse.i18n import RCSEMessageFactory
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.mediaelementjs.browser.view import File as MediaElementJS

_ = RCSEMessageFactory


class AudioSchema(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    file = NamedBlobFile(title=_(u"Audio file"))


class AudioView(MediaElementJS):
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

    def getFilename(self):
        return self.context.file.filename.encode('utf-8')
