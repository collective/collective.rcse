from plonetheme.jquerymobile.layer import Layer as JQMobileLayer
from plone.app.discussion.interfaces import IDiscussionLayer
from collective.favoriting.layer import Layer as FavLayer
from plone.app.event.interfaces import IBrowserLayer as EventLayer
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from plone.app.z3cform.interfaces import IPloneFormLayer
from collective.whathappened.layer import Layer as WhathappenedLayer
from collective.requestaccess.layer import Layer as RequestAccessLayer


class CommonLayer(
    FavLayer, IDiscussionLayer, EventLayer,
    IPloneAppContenttypesLayer, WhathappenedLayer,
    RequestAccessLayer
):
    """Marker interface which is used in both theme"""


class MobileLayer(CommonLayer, JQMobileLayer):
    """Marker interface which is used in the mobile theme."""


class DesktopLayer(CommonLayer, IPloneFormLayer):
    """Marker interface which is used in the desktop theme"""
