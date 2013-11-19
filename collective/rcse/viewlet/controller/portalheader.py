from plone.app.layout.viewlets.common import ViewletBase, PersonalBarViewlet
from collective.rcse.viewlet.controller import sections
from collective.rcse.viewlet.controller.sections import RCSESections
from collective.whathappened.browser.notifications import HotViewlet
from copy import copy
import urllib

from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from plone.autoform.form import AutoExtensibleForm
from plone.autoform import directives
from plone.supermodel import model
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform import z2
from Products.CMFCore.utils import getToolByName
from z3c.form import form
from z3c.form import button
from z3c.form.interfaces import IFormLayer
from z3c.form.browser.select import SelectFieldWidget
from zope import component
from zope import schema
from zope import interface
from urlparse import parse_qs
from urllib import urlencode
from collective.rcse.content.group import get_group
from collective.rcse.icons import getType
from plonetheme.jquerymobile.browser.viewlets.header import PanelLeftAction,\
    PanelRightAction, GlobalSections, SearchRightAction


class PortalHeaderViewlet(RCSESections, HotViewlet):
    """revamp the header"""

    def update(self):
        RCSESections.update(self)
        HotViewlet.update(self)
        self.context_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state'
        )
        self.portal_properties = getToolByName(self.context,
                                               'portal_properties')
        self.query_str = self.request.get('QUERY_STRING', None)
        self.filter_query = parse_qs(self.query_str)
        self.updateUserName()

    def updateUserName(self):
        self.auth_user = self.context.restrictedTraverse('auth_memberinfo')
        try:
            self.auth_user.update()
            self.user_name = self.auth_user.fullname
        except ValueError:
            self.user_name = ''

    def updateUserActions(self):
        pass

    def filter_url(self, portal_type):
        url = self.context_state.current_base_url()
        #TODO: deserialize
        if self.query_str:
            query = copy(self.filter_query)
            query['portal_type'] = portal_type
            query_str = urlencode(query)
            url += '?' + query_str
        else:
            url += '?portal_type=%s' % portal_type
        return url

    def filter_portal_type(self):
        if self.filter_query:
            return self.filter_query.get('portal_type', None)

    def group_url(self):
        group = get_group(self.context)
        if group is None:
            group_url = self.portal_state.navigation_root_url()
            if not group_url.endswith('/home'):
                group_url += '/home'
        else:
            group_url = group.absolute_url()
        return group_url

    def get_icon(self, term):
        return getType(term)
