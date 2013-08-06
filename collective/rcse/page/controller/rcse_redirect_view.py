from Products.Five.browser import BrowserView


class HomeRedirect(BrowserView):
    """Redirect to /home"""

    def __call__(self):
        self.request.response.redirect('%s/home' % self.context.absolute_url())
