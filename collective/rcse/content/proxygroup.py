import logging

from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five.browser import BrowserView
from plone.dexterity.utils import createContentInContainer, createContent
from plone.directives import form

from zope import interface

logger = logging.getLogger("collective.rcse")


class ProxyGroupSchema(form.Schema):
    """Marker interface"""


class ProxyGroupManager(BrowserView):
    """the default view will display the image title / description of the 
    original group with a button to request access to it.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.group = None
        self.proxy = None

    def __call__(self):
        self.update()
        return self  # to use it in template without 'no-call:' trick

    def update(self):
        self.container = self.context.aq_inner.aq_parent
        ptype = self.context.portal_type

        if ptype == "collective.rcse.group":
            self.group = self.context.aq_inner
            self.group_id = self.group.getId()
            self.proxy_id = "%s_proxy" % self.group_id
            self.proxy = self.container.get(self.proxy_id, None)
        elif ptype == "collective.rcse.proxygroup":
            self.proxy = self.context.aq_inner
            self.proxy_id = self.proxy.getId()
            self.group_id = self.proxy_id[:-len("_proxy")]
            self.group = self.container.get(self.group_id)
        else:
            raise ValueError("context is not group or proxy but %s" % ptype)

        self.portal_workflow = getToolByName(self.context, "portal_workflow")
        self.group_status = self.portal_workflow.getInfoFor(
            self.group, "review_state", None
        )

    def get_proxy(self, pid):
        if not pid.endswith('_proxy'):
            pid += "_proxy"
        return self.container.get(pid, None)

    def title(self):
        return self.group.Title()

    def description(self):
        return self.group.Description()

    def create_or_update_proxy(self):
        if self.group_status != "moderated":
            return
        if self.proxy is None:
            self.proxy = createContent(
                "collective.rcse.proxygroup",
                checkConstraints=False,
                title=self.title(),
                description=self.description()
            )
            self.proxy.id = self.proxy_id
            self.container._setObject(self.proxy_id, self.proxy)
        else:
            #just update the proxy
            if self.proxy.Title() != self.title():
                self.proxy.setTitle(self.title())
            if self.proxy.Description() != self.description():
                self.proxy.setDescription(self.description())

        self.proxy.reindexObject()

    def delete_proxy(self):
        if self.proxy and self.group_status != "moderated":
            self.container.manage_delObjects([self.proxy.getId()])


def handle_group_edit(context, event):
    """update the proxy / Be care about rename action"""
    manager = context.restrictedTraverse("@@proxy_group_manager")
    manager.update()
    manager.create_or_update_proxy()


def handle_group_wfstate_change(context, event):
    """
    #if new state == moderated -> create a proxy space
    #else: delete proxy if exists
    """
    manager = context.restrictedTraverse("@@proxy_group_manager")
    manager.update()
    old_state = event.old_state.id
    new_state = event.status.get('review_state', None)
    if new_state == "moderated":
        manager.create_or_update_proxy()
    elif old_state == "moderated":
        manager.delete_proxy()


def handle_group_removed(context, event):
    wftool = getToolByName(self.context, "portal_workflow")
    status = wftool.getInfoFor(event.object, "review_state")
    if status != "moderated":
        return
    manager = context.restrictedTraverse("@@proxy_group_manager")
    manager.update()
    manager.delete_proxy()


def handle_group_moved(context, event):
    wftool = getToolByName(self.context, "portal_workflow")
    status = wftool.getInfoFor(event.object, "review_state")
    if status != "moderated":
        return
    if event.oldParent != event.newParent:
        event.newParent.manage_pasteObjects(
            event.oldParent.manage_cutObjects(event.oldName + '_proxy')
        )
    else:
        event.newParent.manage_renameObject(
            event.oldName + '_proxy', event.newName + '_proxy'
        )
