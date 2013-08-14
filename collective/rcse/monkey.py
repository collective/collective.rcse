from collective.z3cform.widgets import enhancedtextlines

#Remove this because it's useless for us
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
