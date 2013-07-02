from plone.app.testing import (
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
)

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.testing import z2
from plonetheme.jquerymobile import testing as mobile_testing
import collective.rcse


class Layer(mobile_testing.Layer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        mobile_testing.Layer.setUpZope(self, app, configurationContext)
        self.loadZCML(package=collective.rcse)

    def setUpPloneSite(self, portal):
        mobile_testing.Layer.setUpPloneSite(self, portal)
        self.applyProfile(portal, 'collective.rcse:default')
        from plone import api
        self.ploneapi = api
        self.create_user("simplemember1", "Simple Member 1")
        self.create_user("simplemember2", "Simple Member 2")
        self.create_user("simplemember3", "Simple Member 3")
        roles = ("Member", "Site Administrator")
        self.create_user("siteadmin", "Site Admin", roles=roles)

    def create_user(self, username, fullname, roles=("Member",)):
        self.ploneapi.user.create(
            email="%s@example.com" % username,
            username=username,
            password="secret",
            roles=roles,
            properties={"fullname": fullname}
        )


FIXTURE = Layer()
INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="collective.rcse:Integration"
)

FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,),
    name="collective.rcse:Functional"
)

ROBOT = FunctionalTesting(
    bases=(AUTOLOGIN_LIBRARY_FIXTURE, FIXTURE, z2.ZSERVER),
    name="collective.rcse:Robot")
