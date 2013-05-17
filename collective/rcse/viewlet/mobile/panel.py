from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plonetheme.jquerymobile.browser.viewlets import panel as base


class UserToolBar(base.UserToolBar):

    index = ViewPageTemplateFile('templates/usertoolbar.pt')

    def update(self):
        base.UserToolBar.update(self)
        self.portal_types = getToolByName(self.context, 'portal_types')
        if self.context.portal_type in ("collective.rcse.group", "Plone Site"):
            self.container = self.context
        else:
            self.container = self.context.aq_inner.aq_parent
        self.filters = []
        self.current_filter = None
        if self.request.get('filter', False):
            self.current_filter = self.request.get('portal_type', None)

    def get_filters(self):
        if not self.filters:
            types = self.container.allowedContentTypes()
            for fti in types:
                context_url = self.context.absolute_url()
                url = '%s?filter=1&portal_type=%s' % (context_url, fti.id)
                info = {"url": url, "id": fti.id, "title": fti.Title()}
                info["current"] = False
                if fti.id == self.current_filter:
                    info["current"] = True
                self.filters.append(info)
        return self.filters
