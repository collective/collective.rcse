from plone.app.testing import (
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
    login, logout, setRoles,
    SITE_OWNER_NAME,
    TEST_USER_NAME, TEST_USER_ID, TEST_USER_PASSWORD,
)

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.testing import z2
from plonetheme.jquerymobile import testing as mobile_testing
from Products.CMFCore.utils import getToolByName
import collective.rcse


class Layer(mobile_testing.Layer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        mobile_testing.Layer.setUpZope(self, app, configurationContext)
        import plone.app.versioningbehavior
        self.loadZCML(package=plone.app.versioningbehavior)
        self.loadZCML(package=collective.rcse)

    def setUpPloneSite(self, portal):
        mobile_testing.Layer.setUpPloneSite(self, portal)
        self.applyProfile(portal, 'plone.app.versioningbehavior:default')
        self.applyProfile(portal, 'collective.rcse:default')
#        login(portal, SITE_OWNER_NAME)  raise an exception ...
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.create_user(portal, "simplemember1")
        self.create_user(portal, "simplemember2")
        self.create_user(portal, "simplemember3")
        self.create_user(portal, "siteadmin", role="Site Administrator")

        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain('intranet_workflow')

        logout()

    def create_user(self, portal, username, role="Member"):
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser(username, TEST_USER_PASSWORD, [role], [])
#        self.ploneapi.user.create(
#            email="%s@example.com" % username,
#            username=username,
#            password="secret",
#            roles=(role,),
#            properties={"fullname": fullname}
#        )


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
