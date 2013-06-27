from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from Products.Five.browser import BrowserView
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class FileSchema(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    file = NamedBlobFile(title=_(u"File"))


class FileView(BrowserView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        context_url = self.context.absolute_url()
        self.filename = self.context.file.filename.encode('utf-8')
        self.download_url = context_url + '/@@download/file/' + self.filename
        self.mimetype = self.context.file.contentType
