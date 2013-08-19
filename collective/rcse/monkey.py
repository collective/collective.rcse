import logging
from collective.z3cform.widgets import enhancedtextlines

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
    from collective.rcse.layer import MobileLayer
    original_render = ContentTreeBase.render
    def render(self):
        if MobileLayer.providedBy(self.request):
            return u"This feature is not supported"
        else:
            return original_render(self)
    ContentTreeBase.render = render

patch_contenttree()
