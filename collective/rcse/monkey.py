import logging
from AccessControl.unauthorized import Unauthorized
from Acquisition import aq_parent
from collective.z3cform.widgets import enhancedtextlines
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


def patch_contenttree():
    from plone.formwidget.contenttree.widget import ContentTreeBase
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


logger.info("monkeypatch: Remove contenttree for mobile")
patch_contenttree()


def patch_event():
    from plone.app.event.dx.behaviors import EventAccessor
    EventAccessor.event_type = 'collective.rcse.event'


logger.info("monkey: change content_type for plone.app.event")
patch_event()


def patch_get_calendar_url():
    from plone.app.event import portlets
    from collective.rcse.content.group import get_group

    def get_calendar_url(context, search_base):
        portal_state = context.restrictedTraverse('plone_portal_state')
        navigation_root = portal_state.navigation_root()
        if search_base:
            base = navigation_root.restrictedTraverse(search_base.lstrip('/'))
            return base.absolute_url()
        else:
            group = get_group(context)
            if group is None:
                group = navigation_root
            return '%s/event_listing' % group.absolute_url()
    portlets.get_calendar_url = get_calendar_url


logger.info("monkeypatch: Get group for url for plone.app.event portlets")
patch_get_calendar_url()


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
        except TypeError:
            return True
        if not dm.canAccess():
            return True
        return False

    from z3c.form import util
    util.changedField = changedField


logger.info("monkey: z3c.form.util.changedField handle naive date exception")
patch_z3cform()


def patch_whathappened():
    def _getSubscriptionInTree(self, path):
        context = None
        while '/' in path and path != '/':
            subscription = self.storage.getSubscription(path)
            if subscription is not None:
                break
            try:
                if context is None:
                    context = self.context.restrictedTraverse(path)
                else:
                    context = aq_parent(context)
                if context.portal_type == 'collective.rcse.group':
                    break
            except KeyError:
                pass
            except Unauthorized:
                pass
            path = path.rpartition('/')[0]
        return subscription

    from collective.whathappened.gatherer_backend \
        import UserActionGathererBackend
    UserActionGathererBackend._getSubscriptionInTree = _getSubscriptionInTree


logger.info("monkey: change whathappened gatherer to stop at group")
patch_whathappened()
