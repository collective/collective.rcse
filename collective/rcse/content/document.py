from plone.directives import form
from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg.widget import WysiwygFieldWidget
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class DocumentSchema(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    form.widget(text=WysiwygFieldWidget)
    text = RichText(title=_(u"Text"))
