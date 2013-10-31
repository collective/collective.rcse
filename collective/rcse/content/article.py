from zope import interface
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from collective.rcse.i18n import RCSEMessageFactory
from plone.rfc822.interfaces import IPrimaryField
from plone.app.textfield import RichText
from plone.app.contenttypes.interfaces import IDocument
from Products.CMFPlone import PloneMessageFactory as _p
_ = RCSEMessageFactory


class ArticleSchema(form.Schema, IDocument):
    """An audio file.
    """

    image = NamedBlobImage(title=_(u"Image"),
                           required=False)
    text = RichText(title=_p(u"Text"),
                    required=False)

interface.alsoProvides(ArticleSchema['text'], IPrimaryField)
