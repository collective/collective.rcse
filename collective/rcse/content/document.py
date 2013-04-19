from plone.directives import form
from Products.Five.browser import BrowserView
from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg.widget import WysiwygFieldWidget
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class DocumentSchema(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    form.widget(text=WysiwygFieldWidget)
    text = RichText(title=_(u"Text"))


class DocumentView(BrowserView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        pass