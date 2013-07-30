from plone.autoform.interfaces import WIDGETS_KEY
from plone.app.event.dx.behaviors import IEventBasic
from collective.z3cform.html5widgets.widget_datetime import DateTimeWidget


#override event basic widgets
IEventBasic.setTaggedValue(
    WIDGETS_KEY, {'start': DateTimeWidget,
                  'end': DateTimeWidget}
)
