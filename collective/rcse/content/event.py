from zope import schema
from plone.autoform.interfaces import WIDGETS_KEY
from plone.app.event.dx.behaviors import IEventBasic
from plone.supermodel import model
from plone.namedfile.field import NamedBlobImage
from collective.rcse.i18n import _
from collective.z3cform.html5widgets.widget_datetime import DateTimeWidget


#override event basic widgets
IEventBasic.setTaggedValue(
    WIDGETS_KEY, {'start': DateTimeWidget,
                  'end': DateTimeWidget}
)


class EventSchema(model.Schema):
    """event extra fields"""
    image = NamedBlobImage(title=_(u"Image"),
                          description=_(u"image_description"),
                           required=False)
    urlMedia = schema.URI(title=_(u"Media URL"),
                          description=_(u"urlMedia_description"),
                          required=False)
    urlGMaps = schema.URI(title=_(u"Google Maps URL"),
                          description=_(u"urlGMaps_description"),
                          required=False)
