from zope import interface
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from collective.rcse.i18n import RCSEMessageFactory
from plone.rfc822.interfaces import IPrimaryField

_ = RCSEMessageFactory


class AudioSchema(form.Schema):
    """An audio file.
    """

    file = NamedBlobFile(title=_(u"Audio file"))

interface.alsoProvides(AudioSchema['file'], IPrimaryField)
