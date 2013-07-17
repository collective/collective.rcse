from collective.rcse.page.controller.group_base import BaseView


class FavoritesView(BaseView):
    """A filterable timeline"""
    filter_type = ["collective.rcse.favorite"]
