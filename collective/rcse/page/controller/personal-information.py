from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope import component

class PersonalInformation(BrowserView):
    """Redirect to @@register_information if the user has not created his
    content yet. Redirect to his content otherwise."""

    def getMemberInfo(self):
        self.portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
            )
        self.member = self.portal_state.member()
        #get member data
        catalog = getToolByName(self.context, 'membrane_tool')
        self.username = self.member.getUserName()
        self.member_data = None
        if self.username:
            results = catalog(getUserName=self.username)
            if results:
                self.member_data = results[0].getObject()

    def __call__(self):
        self.getMemberInfo()
        portal_url = self.portal_state.portal_url()
        if self.portal_state.anonymous():
            self.request.response.redirect(
                '%s/@@register' % portal_url
                )
            return
        if self.username == 'admin':
            self.request.response.redirect(
                '%s/users_directory' % portal_url
                )
        elif self.member_data is None:
            self.request.response.redirect(
                '%s/@@register_information' % portal_url
                )
        else:
            self.request.response.redirect(
                '%s/edit' % self.member_data.absolute_url()
                )
