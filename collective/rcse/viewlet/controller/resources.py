from plone.app.layout.viewlets.common import ViewletBase


class ResourcesViewlet(ViewletBase):
    """Display resources for RCSE"""
    def __call__(self):
        self.update()
        return super(ResourcesViewlet, self).__call__()
