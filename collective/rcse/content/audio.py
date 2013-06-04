from plone.namedfile.field import NamedBlobFile
from collective.rcse.content import common
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class AudioSchema(common.RCSEContent):
    """A conference session. Sessions are managed inside Programs.
    """

    file = NamedBlobFile(title=_(u"Audio file"))
