from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class VideoSchema(form.Schema):
    """A video file"""

    file = NamedBlobFile(title=_(u"Video file"))
