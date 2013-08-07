from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


class PersonalInformation(BrowserView):
    """Redirect to @@register_information if the user has not created his
    content yet. Redirect to his content otherwise."""

    def __call__(self):
        portal_url = getToolByName(self.context, 'portal_url')
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if member.getId() == 'admin':
            self.request.response.redirect(
                '%s/users_directory' % portal_url()
                )
        elif type(member.getProperty('username')) == object:
            self.request.response.redirect(
                '%s/@@register_information' % portal_url()
                )
        else:
            catalog = getToolByName(self.context, 'membrane_tool')
            results = catalog(getUserName=member.getProperty('username'))
            if len(results) == 0:
                self.request.response.redirect(
                    '%s/users_directory' % portal_url()
                    )
            else:
                self.request.response.redirect(
                    results[0].getURL()
                    )
