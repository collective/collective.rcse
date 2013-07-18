from Products.Five.browser import BrowserView


class CompaniesDirectoryView(BrowserView):
    """View for the users directory."""

    def __call__(self):
        return self.index()
