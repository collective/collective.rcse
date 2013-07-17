from collective.rcse.page.controller.group_base import BaseView


class AudiosView(BaseView):
    """A filterable timeline"""
    filter_type = set("collective.rcse.audio")
