from zope.i18n import translate
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class GroupEditView(BrowserView):
    """@@rcse_group_edit view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.workflow = getToolByName(self.context, 'portal_workflow')

        query = {"path": "/".join(self.context.getPhysicalPath())}
        self.how_many_contents = len(self.catalog(**query))
        self.rmanager = self.context.restrictedTraverse("request_manager")

        query = {"target_path": '/'.join(self.context.getPhysicalPath())}
        self.how_many_requests = len(self.rmanager.get(query=query))

        review_state = self.workflow.getInfoFor(self.context, 'review_state')
        self.review_state = translate(review_state,
                                      domain="plone",
                                      context=self.request)

    def can_edit(self):
        return True

    def can_rename(self):
        return True

    def can_delete(self):
        return True

    def can_manage_portlets(self):
        return True

    def can_select_default_view(self):
        return True

    def can_list_folder_contents(self):
        return True

    def can_invite_person(self):
        return True

    def can_manage_request_access(self):
        return True

    def can_change_status(self):
        return True
