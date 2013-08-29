from plone.app.layout.viewlets.common import ViewletBase, PersonalBarViewlet
from collective.rcse.viewlet.controller import sections
from collective.rcse.viewlet.controller.sections import RCSESections
from collective.whathappened.browser.notifications import HotViewlet


class PortalHeaderViewlet(RCSESections, HotViewlet):
    """revamp the header"""

    def update(self):
        RCSESections.update(self)
        PersonalBarViewlet.update(self)
        HotViewlet.update(self)


    def updateUserActions(self):
        pass
