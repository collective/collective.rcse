from plone.app.testing import (
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
    login, logout, setRoles,
    TEST_USER_NAME, TEST_USER_ID, TEST_USER_PASSWORD,
    SITE_OWNER_NAME,
)

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.testing import z2
#import layers from addons
from plonetheme.jquerymobile import testing as mobile_testing
from plone.app.event import testing as event_testing
from plone.app.contenttypes import testing as ptypes_testing
from Products.CMFCore.utils import getToolByName
import collective.rcse
import transaction


class Layer(mobile_testing.Layer,
            event_testing.PAEventLayer,
            event_testing.PAEventDXLayer,
            ptypes_testing.PloneAppContenttypes):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        mobile_testing.Layer.setUpZope(self, app, configurationContext)
        event_testing.PAEventLayer.setUpZope(self, app, configurationContext)
        event_testing.PAEventDXLayer.setUpZope(self, app, configurationContext)
        ptypes_testing.PloneAppContenttypes.setUpZope(self, app, configurationContext)
        import plone.app.versioningbehavior
        import five.localsitemanager
        import Products.membrane
        import plone.app.contentrules
        self.loadZCML(package=plone.app.versioningbehavior)
        self.loadZCML(package=plone.app.contentrules)
        self.loadZCML(package=five.localsitemanager)
        self.loadZCML(package=Products.membrane)
        z2.installProduct(app, 'Products.membrane')  # initialize
        self.loadZCML(package=collective.rcse)

    def setUpPloneSite(self, portal):
        #make global request work
#        from five.globalrequest import hooks
#        class FakeEvent:
#            def __init__(self, request):
#                self.request = request
#        event = FakeEvent(portal.REQUEST)
#        hooks.set_(event)
#        from five.localsitemanager import make_objectmanager_site
#        make_objectmanager_site(portal)

        mobile_testing.Layer.setUpPloneSite(self, portal)
        event_testing.PAEventLayer.setUpPloneSite(self, portal)
        event_testing.PAEventDXLayer.setUpPloneSite(self, portal)
        ptypes_testing.PloneAppContenttypes.setUpPloneSite(self, portal)
        self.applyProfile(portal, 'plone.app.versioningbehavior:default')
        self.applyProfile(portal, 'collective.rcse:default')
        #The setup unactivate source users to use CAS. because we are in test
        #we just reactivate sources users
        portal.acl_users.source_users.manage_activateInterfaces([
            "IAuthenticationPlugin",
            "IUserAdderPlugin",
            "IUserEnumerationPlugin",
            #"IUserIntrospection",
            #"IUserManagement",
        ])
        login(portal, SITE_OWNER_NAME)
#        login(portal, TEST_USER_NAME)
#        setRoles(portal, TEST_USER_ID, ['Manager'])
#        transaction.commit()
        self.create_user(portal, "simplemember1")
#        self.create_user(portal, "simplemember2")
#        self.create_user(portal, "simplemember3")
#        self.create_user(portal, "siteadmin", role="Site Administrator")

        logout()

    def create_user(self, portal, username, role="Member"):
#        acl_users = getToolByName(portal, 'acl_users')
#        acl_users.userFolderAddUser(username, TEST_USER_PASSWORD, [role], [])
        regtool = getToolByName(portal, 'portal_registration')
        regtool.addMember(username, username)
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
