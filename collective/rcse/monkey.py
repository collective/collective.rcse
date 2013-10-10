import logging
from collective.z3cform.widgets import enhancedtextlines
from Products.CMFPlone.PloneBatch import Batch
from zope.schema.interfaces import IObject
from zope.component._api import getMultiAdapter
from z3c.form.interfaces import IDataManager

logger = logging.getLogger("collective.rcse")

logger.info("monkeypatch: EnhancedTextLinesWidget do nothing if no taskplease")
enhancedtextlines.EnhancedTextLinesWidget.js_template = """\
    (function($) {
        $().ready(function() {
        tp_i18n = {
            add:'%(add)s',
            add_task:'%(add_task)s',
            delete_task:'%(delete_task)s',
            edit_task:'%(edit_task)s'
        }
        if(jQuery().taskplease) {
             $('#%(id)s').tasksplease();
        }
        });
    })(jQuery);
"""


logger.info("monkeypatch: Remove contenttree for mobile")
def patch_contenttree():
    from plone.formwidget.contenttree.widget import ContentTreeBase
    from plone.browserlayer import utils
    from collective.rcse import layer
    original_render = ContentTreeBase.render
    def render(self):
        if layer.MobileLayer.providedBy(self.request):
            return u"This feature is not supported"
        elif layer.DesktopLayer.providedBy(self.request):
            return u"This feature is not supported"
        else:
            return original_render(self)
    ContentTreeBase.render = render

patch_contenttree()


logger.info("monkey: fix batching")
def patch_batch():
    def batchgetitem(self, index):
        """ Get item from batch
        """
        #this doesn't work at all .... lets remove this
        #actual = getattr(self._sequence, 'actual_result_count', None)
        #if actual is not None and actual != len(self._sequence):
            # optmized batch that contains only the wanted items in the
            # sequence
        #    return self._sequence[index]
        if index < 0:
            if index + self.end < self.first:
                raise IndexError(index)
            return self._sequence[index + self.end]
        if index >= self.length:
            raise IndexError(index)
        return self._sequence[index + self.first]
    Batch.__getitem__ = batchgetitem

patch_batch()


logger.info("monkey: change content_type for plone.app.event")
def patch_event():
    from plone.app.event.dx.behaviors import EventAccessor
    EventAccessor.event_type = 'collective.rcse.event'

patch_event()


logger.info("monkey: z3c.form.util.changedField handle naive date exception")
def patch_z3cform():
    """TypeError: can't compare offset-naive and offset-aware datetimes
    """
    def changedField(field, value, context=None):
        """Figure if a field's value changed

        Comparing the value of the context attribute and the given value"""
        if context is None:
            context = field.context
        if context is None:
            # IObjectWidget madness
            return True
        if IObject.providedBy(field):
            return True

        # Get the datamanager and get the original value
        dm = getMultiAdapter(
            (context, field), IDataManager)
        # now figure value chaged status
        # Or we can not get the original value, in which case we can not check
        # Or it is an Object, in case we'll never know
        try:
            test = dm.query() != value
            if test:
                return True
        except TypeError as e:
            return True
        if not dm.canAccess():
            return True
        return False

    from z3c.form import util
    util.changedField = changedField

patch_z3cform()
