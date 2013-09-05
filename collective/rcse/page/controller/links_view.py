from collective.rcse.page.controller.group_base import BaseView
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView


class LinksView(BaseView):
    """A filterable timeline"""
    filter_type = ["Link"]


class NavigationRootLinksView(LinksView, NavigationRootBaseView):
    def update(self):
        LinksView.update(self)
        NavigationRootBaseView.update(self)
