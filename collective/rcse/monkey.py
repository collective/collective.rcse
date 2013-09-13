import logging
from collective.z3cform.widgets import enhancedtextlines
from Products.CMFPlone.PloneBatch import Batch

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
