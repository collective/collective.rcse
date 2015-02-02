from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from plone.rfc822.interfaces import IPrimaryField
from plone.app.textfield import RichText
from plone.app.contenttypes.interfaces import IDocument
from Products.CMFPlone import PloneMessageFactory as _p
from zope import interface
from zope import schema

from collective.rcse.content import vocabularies
from collective.rcse.i18n import RCSEMessageFactory

_ = RCSEMessageFactory


class ArticleSchema(form.Schema, IDocument):
    """An audio file.
    """

    image = NamedBlobImage(title=_(u"Image"),
                           required=False)
    image_position = schema.Choice(
        title=_(u"Image position"),
        vocabulary=vocabularies.image_position,
        required=False
    )
    text = RichText(title=_p(u"Text"),
                    required=False)

interface.alsoProvides(ArticleSchema['text'], IPrimaryField)
