from collective.requestaccess.browser.request import CancelRequestForm,\
    ValidationRequestForm
from Products.Five.browser import BrowserView
from z3c.form.interfaces import HIDDEN_MODE
from zope import component

import logging
logger = logging.getLogger("collective.requestaccess")


class MyRequestsView(BrowserView):
    """requests view"""
    form_class = CancelRequestForm

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.manager = None
        self.tools = None
        self.portal_state = None
        self.userid = None
        self.requests = None
        self.invites = None
        self.query = None
        self.dependency_loaded = False

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        if not self.dependency_loaded:
            self.tools = component.getMultiAdapter(
                (self.context, self.request),
                name="plone_tools",
            )
            self.portal_state = component.getMultiAdapter(
                (self.context, self.request),
                name="plone_portal_state",
            )
            self.manager = self.context.restrictedTraverse("request_manager")
            mtool = self.tools.membership()
            self.userid = mtool.getAuthenticatedMember().getId()
            self.dependency_loaded = True
        if self.requests is None:
            self.requests = []
            requests = self.manager.get(query=self.get_query())
            for request in requests:
                info = self.get_request_info(request)
                form = self.form_class(self.context, self.request)
                form.next_url = self.get_next_url()
                form.prefix = info["id"]
                form.update()
                form.widgets["requestaccessid"].mode = HIDDEN_MODE
                form.widgets["requestaccessid"].value = info["id"]
                info["form"] = form
                self.requests.append(info)

        if self.invites is None:
            self.invites = []
            query = {"rtype": "invitation", "userid": self.userid}
            requests = self.manager.get(query=query)
            for request in requests:
                info = self.get_request_info(request)
                form = ValidationRequestForm(self.context, self.request)
                form.next_url = self.get_next_url()
                form.prefix = info["id"]
                form.update()
                form.widgets["requestaccessid"].mode = HIDDEN_MODE
                form.widgets["requestaccessid"].value = info["id"]
                info["form"] = form
                self.invites.append(info)

    def get_query(self):
        return {"userid": self.userid, "rtype": "request"}

    def get_request_info(self, request):
        url = self.portal_state.navigation_root_url() + "/resolveuid/"
        ppath = self.portal_state.portal().getPhysicalPath()
        rpath = request.target_path
        target_path = rpath[len(ppath):]
        return {
            "id": request.id,
            "role": request.role,
            "creatorid": request.creatorid,
            "userid": request.userid,
            "target": url + request.target,
            "target_path": '/'.join(target_path),
            "target_title": request.target_title,
        }

    def get_next_url(self):
        return self.context.absolute_url() + '/@@my_requests_view'


class ReviewRequestsView(MyRequestsView):
    form_class = ValidationRequestForm

    def get_next_url(self):
        return self.context.absolute_url() + '/@@review_requests_view'

    def get_query(self):
        return {"target_path": '/'.join(self.context.getPhysicalPath())}
