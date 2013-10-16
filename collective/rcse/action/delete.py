from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from collective.rcse.i18n import _
from z3c.form import form, button
from plone.z3cform.layout import FormWrapper
from Products.statusmessages import STATUSMESSAGEKEY
from zope.annotation.interfaces import IAnnotations
from collective.rcse.utils import sudo

class DeleteForm(form.Form):
    enableCSRFProtection = True

    @button.buttonAndHandler(_("Delete"))
    def handleDelete(self, action):
        self._doDelete()

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

        parent_url = self.context.aq_inner.aq_parent.absolute_url()
        self.request.response.redirect(parent_url)


class Delete(FormWrapper):
    form = DeleteForm
    def label(self):
        return _(u"Are you sure you want to delete ${title} and all it's content ?",
                 mapping={"title": self.context.Title()})
