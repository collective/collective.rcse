from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from Products.Five.browser import BrowserView
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class ImageSchema(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    image = NamedBlobImage(title=_(u"Image"))


class ImageView(BrowserView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        context_url = self.context.absolute_url()
        self.filename = self.context.image.filename.encode('utf-8')
        self.download_url = context_url + '/@@download/image/' + self.filename
        self.mimetype = self.context.image.contentType
