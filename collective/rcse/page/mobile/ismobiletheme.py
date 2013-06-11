from Products.Five.browser import BrowserView


class IsMobileTheme(BrowserView):
    """This view is used to display themeswitcher action in the
    footer"""
    def __call__(self):
        return True
