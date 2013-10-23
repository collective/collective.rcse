from plone.app.portlets.browser import manage
from collective.rcse.content.group import get_group


class ManageContextualPortlets(manage.ManageContextualPortlets):
    def __call__(self):
        group = get_group(self.context)
        if group is not None and group != self.context:
            url = group.absolute_url() + '/@@manage-portlets'
            self.request.response.redirect(url)
            return
        return super(ManageContextualPortlets, self).__call__()
