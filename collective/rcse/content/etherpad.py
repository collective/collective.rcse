from plone.directives import form
from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg.widget import WysiwygFieldWidget
from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.content import common

_ = RCSEMessageFactory


class EtherpadSchema(common.RCSEContent):
    """A conference session. Sessions are managed inside Programs.
    """
