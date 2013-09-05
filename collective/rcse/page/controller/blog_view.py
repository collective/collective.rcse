from collective.rcse.page.controller.group_base import BaseView
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView


class BlogView(BaseView):
    """A filterable timeline"""
    filter_type = ["News Item"]


class NavigationRootBlogView(BlogView, NavigationRootBaseView):
    def update(self):
        BlogView.update(self)
        NavigationRootBaseView.update(self)
