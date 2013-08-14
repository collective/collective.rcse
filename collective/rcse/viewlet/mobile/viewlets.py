from plonetheme.jquerymobile.browser.viewlets import personal_bar

from plone.app.layout.viewlets.common import ViewletBase


class GroupDisplayMenu(ViewletBase):
    def update(self):
        super(GroupDisplayMenu, self).update()
        layouts = self.context.getAvailableLayouts()
        selected = self.context.getLayout()
        defaultPage = self.context.getDefaultPage()
        contextUrl = self.context.absolute_url()
        self.available_layouts = []
        for id, title in layouts:
            is_selected = (defaultPage is None and id == selected)
            self.available_layouts.append({
                'title': title,
                'description': '',
                'url': '%s/%s' % (contextUrl, id,),
                'selected': is_selected,
                'icon': None,
            })
