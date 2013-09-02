from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from collective.rcse.i18n import RCSEMessageFactory
from zope import schema
from Products.CMFPlone import PloneMessageFactory

_ = RCSEMessageFactory


class DiscussionSchema(form.Schema):
    """An audio file.
    """
    title = schema.TextLine(title=PloneMessageFactory(u"Title"))
    body = schema.Text(title=_(u"Subject"))
    file = NamedBlobFile(title=_(u"Audio file"),
                         required=False)
