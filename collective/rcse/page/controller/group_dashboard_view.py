from Products.Five.browser import BrowserView


class DashboardView(BrowserView):
    """make a dashboard view which is responsive"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        pass
