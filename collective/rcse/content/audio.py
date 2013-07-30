from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class AudioSchema(form.Schema):
    """An audio file.
    """

    file = NamedBlobFile(title=_(u"Audio file"))
