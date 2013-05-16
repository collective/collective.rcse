from plone.app.layout.viewlets.common import ViewletBase


class HiddenViewlet(ViewletBase):
    """Use this viewlet with the layer you want (mobile / desktop)
    to hide a viewlet.

    Use this instead of viewlets.xml which is not enought flexible
    with skinname. If you create a new skin based on this one you will have
    to copy/paste the viewlets.xml and update all skinnames.

    Using this approch you will just have to make your browser layer inherits
    from the collective.rcse.layer
    """

    def update(self):
        pass

    def index(self):
        return ""
