from plone.autoform.interfaces import WIDGETS_KEY
from plone.app.event.dx.behaviors import IEventBasic
from zope import schema as _schema 
from collective.z3cform.html5widgets.widget_datetime import DateTimeWidget,\
    DateTimeFieldWidget

#override event basic widgets
IEventBasic.setTaggedValue(
    WIDGETS_KEY, {'start': DateTimeFieldWidget,
                  'end': DateTimeFieldWidget}
)
