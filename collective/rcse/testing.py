from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
)

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.testing import z2
from plonetheme.jquerymobile import testing as mobile_testing


class Layer(mobile_testing.Layer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        mobile_testing.Layer.setUpZope(self, app, configurationContext)
        import collective.rcse
        self.loadZCML(package=collective.rcse)

    def setUpPloneSite(self, portal):
        mobile_testing.Layer.setUpPloneSite(self, portal)
        self.applyProfile(portal, 'collective.rcse:default')


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
