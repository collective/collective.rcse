from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage
from Products.statusmessages import STATUSMESSAGEKEY
from Products.CMFCore.utils import getToolByName
from plone.z3cform.layout import FormWrapper
from z3c.form import form, button
from zope import component
from zope.annotation.interfaces import IAnnotations

from collective.rcse.content.group import get_group
from collective.rcse.i18n import _
from collective.rcse.utils import sudo


class DeleteForm(form.Form):
    enableCSRFProtection = True

    @button.buttonAndHandler(_("Delete"))
    def handleDelete(self, action):
        self._doDelete()

    @button.buttonAndHandler(_("Cancel"))
    def handleCancel(self, action):
        context_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state'
        )
        self.request.response.redirect(context_state.view_url())

    @sudo()
    def _doDelete(self):
        wf = self.context.restrictedTraverse('folder_publish')
        ##parameters=workflow_action=None, paths=[], comment='No comment',
        ##expiration_date=None, effective_date=None, include_children=False
        wf(workflow_action="delete",
           comment="RCSE Delete action",
           include_children=True,
           paths=['/'.join(self.context.getPhysicalPath())])
        status = IStatusMessage(self.request)
        # lets replace the message from folder_publish by ours.
        status.show()
        self.request.cookies[STATUSMESSAGEKEY] = None
        self.request.response.expireCookie(STATUSMESSAGEKEY, path='/')
        annotations = IAnnotations(self.request)
        annotations[STATUSMESSAGEKEY] = None
        status.add(_(u"Item and it's content has been deleted"))
        # avoid getting the context itself if it's a group
        group = get_group(aq_inner(self.context).__parent__)
        if group is None:
            url = getToolByName(self.context, 'portal_url')()
        else:
            url = group.absolute_url()
        self.request.response.redirect(url)


class Delete(FormWrapper):
    form = DeleteForm

    def label(self):
        title = self.context.Title()
        if type(title) == str:
            title = title.decode('utf-8')
        return _(u"Are you sure you want to delete "
                 u"${title} and all it's content ?",
                 mapping={"title": title})


class DeleteComment(Delete):
    def label(self):
        return _(u"Are you sure you want to delete this comment ?")
