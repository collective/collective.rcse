from collective.rcse.viewlet.controller.portalheader import PortalHeaderViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plonetheme.jquerymobile.browser.viewlets.header import PanelLeftAction,\
    PanelRightAction, GlobalSections, SearchRightAction
from collective.whathappened.browser.notifications import HotViewlet


class PortalHeaderViewletMobile(PortalHeaderViewlet):
    notifications_pt = ViewPageTemplateFile("templates/notifications.pt")
    sections_pt = ViewPageTemplateFile("templates/sections.pt")

    def action_open_left_panel_html(self):
        if not self.user_name:
            return u""
        viewlet = PanelLeftAction(self.context, self.request, self)
        viewlet.update()
        return viewlet.render()

    def action_open_right_panel_html(self):
        if not self.user_name:
            return u""
        viewlet = PanelRightAction(self.context, self.request, self)
        viewlet.update()
        return viewlet.render()

    def action_open_notifications_html(self):
        viewlet = HotViewlet(self.context, self.request, self)
        viewlet.index = self.notifications_pt
        viewlet.update()
        return viewlet.render()

    def action_open_globalsections_html(self):
        if not self.user_name:
            return u""
        viewlet = GlobalSections(self.context, self.request, self)
        viewlet.index = self.sections_pt
        viewlet.update()
        return viewlet.render()

    def action_open_search_html(self):
        if not self.user_name:
            return u""
        viewlet = SearchRightAction(self.context, self.request, self)
        viewlet.update()
        return viewlet.render()
