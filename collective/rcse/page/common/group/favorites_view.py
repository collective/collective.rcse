from collective.rcse.page.common.group import base


class FavoritesView(base.BasedView):
    """A filterable timeline"""
    filter_type = "collective.rcse.favorite"
