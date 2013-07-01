from plone.app.textfield import RichText
from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.content import common

_ = RCSEMessageFactory


class DocumentSchema(common.RCSEContent):
    """A conference session. Sessions are managed inside Programs.
    """

    text = RichText(title=_(u"Text"))
