from Products.Five.browser import BrowserView


class DocumentView(BrowserView):
    """default view"""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        pass
