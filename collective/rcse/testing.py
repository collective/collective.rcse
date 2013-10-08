from plone.app.testing import (
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
    login, logout, setRoles,
    TEST_USER_NAME, TEST_USER_ID, TEST_USER_PASSWORD,
    SITE_OWNER_NAME,
)
from plone.app.testing import selenium_layers

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.testing import z2
#import layers from addons
from plonetheme.jquerymobile import testing as mobile_testing
from plone.app.event import testing as event_testing
from plone.app.contenttypes import testing as ptypes_testing
from Products.CMFCore.utils import getToolByName
from plone.dexterity import utils

import collective.rcse
import transaction
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent, ObjectAddedEvent


class Layer(mobile_testing.Layer,
            event_testing.PAEventLayer,
            event_testing.PAEventDXLayer,
            ptypes_testing.PloneAppContenttypes):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        mobile_testing.Layer.setUpZope(self, app, configurationContext)
        event_testing.PAEventLayer.setUpZope(self, app, configurationContext)
        event_testing.PAEventDXLayer.setUpZope(self, app, configurationContext)
        ptypes_testing.PloneAppContenttypes.setUpZope(self, app, configurationContext)
        import cioppino.twothumbs
        import collective.etherpad
        import collective.favoriting
        import collective.fontawesome
        import collective.history
        import collective.js.ckeditor
        import collective.js.datatables
        import collective.js.jquerymobile
        import collective.mediaelementjs
        import collective.oembed
        import collective.picturefill
        import collective.polls
        import collective.portlet.favoriting
        import collective.portlet.localusers
        import collective.readitlater
        import collective.requestaccess
#        import collective.subscribe
        import collective.themeswitcher
        import collective.transcode.star
        import collective.watcherlist
        import collective.whathappened
        import dexterity.membrane
#        import plone.app.async
        import plone.app.dexterity
        import plone.app.versioningbehavior
        #import plone.app.contenttypes
        #import plone.app.event
        import plone.app.collection
        import plone.namedfile
        import collective.z3cform.html5widgets
#        import plonetheme.jquerymobile

        import collective.js.jqueryui
        import plone.app.versioningbehavior
        import five.localsitemanager
        import collective.indexing
        import Products.membrane
        import plone.app.contentrules

        self.loadZCML(package=collective.history)
        self.loadZCML(package=collective.js.ckeditor)
        self.loadZCML(package=collective.js.datatables)
        self.loadZCML(package=collective.js.jquerymobile)
        self.loadZCML(package=collective.mediaelementjs)
        self.loadZCML(package=collective.oembed)
        self.loadZCML(package=collective.picturefill)
        self.loadZCML(package=collective.polls)
        self.loadZCML(package=collective.portlet.favoriting)
        self.loadZCML(package=collective.portlet.localusers)
        self.loadZCML(package=collective.readitlater)
        self.loadZCML(package=collective.requestaccess)
#        self.loadZCML(package=collective.subscribe)
        self.loadZCML(package=collective.themeswitcher)
        self.loadZCML(package=collective.transcode.star)
        self.loadZCML(package=collective.watcherlist)
        self.loadZCML(package=collective.whathappened)
        self.loadZCML(package=dexterity.membrane)
#        self.loadZCML(package=plone.app.async)
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=plone.app.versioningbehavior)
        #self.loadZCML(package=plone.app.contenttypes)
        #self.loadZCML(package=plone.app.event)
        self.loadZCML(package=plone.app.collection)
        self.loadZCML(package=plone.namedfile)
        self.loadZCML(package=collective.z3cform.html5widgets)
        self.loadZCML(package=plonetheme.jquerymobile)

        self.loadZCML(package=collective.js.jqueryui)
        self.loadZCML(package=plone.app.versioningbehavior)
        self.loadZCML(package=plone.app.contentrules)
        self.loadZCML(package=five.localsitemanager)
        self.loadZCML(package=collective.indexing)
        self.loadZCML(package=Products.membrane)
        z2.installProduct(app, 'Products.membrane')  # initialize
        self.loadZCML(package=collective.rcse)

    def setUpPloneSite(self, portal):
        #make global request work
        from zope.globalrequest import setRequest
        setRequest(portal.REQUEST)
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
        self.applyProfile(portal, 'Products.membrane:default')
        self.applyProfile(portal, 'plone.app.versioningbehavior:default')
        self.applyProfile(portal, 'collective.rcse:default')

        portal.membrane_tool.user_adder = "rcse"
        portal.membrane_tool.membrane_types.append("collective.rcse.member")
        #The setup unactivate source users to use CAS. because we are in test
        #we just reactivate sources users
        portal.acl_users.source_users.manage_activateInterfaces([
            "IAuthenticationPlugin",
            "IUserAdderPlugin",
            "IUserEnumerationPlugin",
            #"IUserIntrospection",
            #"IUserManagement",
        ])
        self.create_user(portal, "simplemember1")
        self.create_user(portal, "simplemember2")

    def create_user(self, portal, username, role="Member"):
        # https://pypi.python.org/pypi/plone.app.testing/4.2.2#id1
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.source_users.doAddUser(username, 'secret')
        container = portal.users_directory
        portal_type = "collective.rcse.member"
        membrane = utils.createContentInContainer(
            container,
            portal_type,
            checkConstraints=False,
            username=username)
        event = ObjectAddedEvent(
            membrane, newParent=container, newName=membrane.getId()
        )
        notify(event)

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
