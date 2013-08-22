from Acquisition import aq_inner, aq_parent
from plone.app.layout.viewlets.common import ViewletBase, ContentViewsViewlet,\
    ContentActionsViewlet
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from zope.component import getMultiAdapter
from plone.app.layout.globals.interfaces import IViewView
from zope.interface.declarations import alsoProvides
from zope.component._api import getUtility, getAdapter, queryAdapter
from zope.browsermenu.interfaces import IBrowserMenu
from plone.stringinterp.interfaces import IStringSubstitution
from Products.CMFCore.WorkflowCore import WorkflowException
from plone.uuid.interfaces import IUUID

MENUS = (
    'plone_contentmenu_actions',
    'plone_contentmenu_display',
    'plone_contentmenu_factory',
    'plone_contentmenu_workflow',
    'plone_contentmenu',
    'plone_displayviews',
)


class EditBar(ViewletBase):
    """Edit bar is a complete revamp to simplify the plone one"""
    def update(self):
        self.membership = getToolByName(self.context, 'portal_membership')
        super(EditBar, self).update()
        self.menus = {}
        for menu in MENUS:
            self.menus[menu] = getUtility(
                IBrowserMenu,
                name=menu,
            ).getMenuItems(self.context, self.request)
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.object_actions = self.context_state.actions('object')

        try:
            adapter = queryAdapter(self.context,
                                   IStringSubstitution,
                                   'review_state_title')
            if adapter:
                self.review_state = adapter()
            else:
                self.review_state = None
        except WorkflowException:
            self.review_state = None
        self.object_uid = IUUID(self.context)


class EditBarView(EditBar):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        return self.index()
