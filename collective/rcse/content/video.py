from zope import schema
from zope.interface import invariant, Invalid
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from collective.rcse.i18n import RCSEMessageFactory
from Products.CMFPlone import PloneMessageFactory
from collective.transcode.star.utility import SETTING_MIME_TYPES
from zope.component._api import getUtility
from plone.registry.interfaces import IRegistry


_ = RCSEMessageFactory
_p = PloneMessageFactory


class InvalidVideo(Invalid):
    __doc__ = _(u"Error raise if no valid video has been provided")


class VideoSchema(form.Schema):
    """A video file"""

    file = NamedBlobFile(title=_(u"Video file"), required=False)
    remoteUrl = schema.URI(
        title=_p(u"URL"),
        required=False
    )

    @invariant
    def validatevideo(data):
        if data.file is None and data.remoteUrl is None:
            msg = _(u"You must provide at least a file or a link")
            raise InvalidVideo(msg)
        if data.file:
            registry = getUtility(IRegistry)
            mime_types = registry[SETTING_MIME_TYPES]
            mime_type = data.file.contentType
            if mime_type not in mime_types:
                msg = _(u"The file must be a video. You are trying to use a "
                        u"'${mime_type}'",
                        mapping={"mime_type": mime_type})
                raise InvalidVideo(msg)
