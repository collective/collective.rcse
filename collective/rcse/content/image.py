from plone.namedfile.field import NamedBlobImage
from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.content import common

_ = RCSEMessageFactory


class ImageSchema(common.RCSEContent):
    """A conference session. Sessions are managed inside Programs.
    """

    image = NamedBlobImage(title=_(u"Image"))
