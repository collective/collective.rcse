from collective.rcse.page.controller.group_base import BaseView


class AlbumsView(BaseView):
    """A filterable timeline"""
    filter_type = set("collective.rcse.album")
