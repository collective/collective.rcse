from collective.rcse.page.controller.group_base import BaseView
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView


class FilesView(BaseView):
    """A filterable timeline"""
    filter_type = ["File"]


class NavigationRootFilesView(FilesView, NavigationRootBaseView):
    def update(self):
        FilesView.update(self)
        NavigationRootBaseView.update(self)
