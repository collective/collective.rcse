from AccessControl import Unauthorized
from Products.Five.browser import BrowserView


class UnauthorizedView(BrowserView):
    def __call__(self):
        raise Unauthorized()
