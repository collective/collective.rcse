from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class ImageSchema(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    image = NamedBlobImage(title=_(u"Image"))
