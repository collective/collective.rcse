from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class DiscussionView(BrowserView):
    """view for the discussion content type aka discussion_view"""
    def __call__(self):
        self.update()
        return self.index()

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.transformer = None

    def update(self):
        if self.transformer is None:
            self.transformer = getToolByName(self.context, "portal_transforms")

    def get_body_as_html(self):
        html = self.convertToHTML(self.context.description, "text/plain")
        return html

    def convertToHTML(self, content, mimetype):
        data = self.transformer.convertTo(
          'text/x-html-safe',
          content.encode('utf-8'),
          mimetype="text/x-web-intelligent",
        )
        result = data.getData()
        if result:
            if isinstance(result, str):
                return unicode(result, 'utf-8')
            return result
