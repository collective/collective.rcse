import os
from plone.app.testing import (
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
    login, logout, setRoles,
    TEST_USER_NAME, TEST_USER_ID, TEST_USER_PASSWORD,
    SITE_OWNER_NAME,
)
from plone.testing import Layer as BaseLayer
from plone.app.testing import selenium_layers

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.testing import z2
from Products.CMFCore.utils import getToolByName
from plone.dexterity import utils

import transaction
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent, ObjectAddedEvent
from plone.app.testing.selenium_layers import SeleniumLayer
from zope.container.interfaces import INameChooser

#import layers from addons
from plonetheme.jquerymobile import testing as mobile_testing
from plone.app.event import testing as event_testing
from plone.app.contenttypes import testing as ptypes_testing
#from plone.app.dexterity import testing as dexterity_testing

from cioppino.twothumbs import testing as twothumbs_testing
from collective.etherpad import testing as etherpad_testing
from collective.favoriting import testing as fav_testing
from collective.fontawesome import testing as font_testing
from collective.history import testing as history_testing
from collective.js.ckeditor import testing as ckeditor_testing
from collective.js.datatables import testing as datatables_testing
#from collective.js.jquerymobile import testings as jqm_testing
#from collective.mediaelementjs import testing as medialement_testing
#from collective.oembed import testing as oembed_testing
#from collective.picturefill import testing as picturefill_testing
from collective.polls import testing as polls_testing
from collective.portlet.favoriting import testing as portlet_fav_testing
from collective.portlet.localusers import testing as portlet_users_testing
from collective.readitlater import testing as readitlayer_testing
from collective.requestaccess import testing as requestacces_testing
from collective.themeswitcher import testing as themeswither_testing
#from collective.transcode.star import testing as star_testing
#from collective.watcherlist import testing as watcherlist_testing
from collective.whathappened import testing as whathappened_testing
from plone.app.testing.layers import PloneFixture
from plone.app.testing.helpers import PloneSandboxLayer
from Testing.ZopeTestCase.utils import setupCoreSessions

from collective.rcse.content.utils import createCompany
from zope.globalrequest import getRequest
from plone.dexterity.utils import createContentInContainer

#class OverrideContentTypesLayer(ptypes_testing.PloneAppContenttypes):
#    """Because we are using a fork of plone.formwidget.autocomplete we need
#    to override plone.app.contenttypes layer which call profile of
#    relation widget with call autocomplete"""
#    def setUpZope(self, app, configurationContext):
#        import collective.js.jqueryui
#        self.loadZCML(package=collective.js.jqueryui)


#PLONE_APP_CONTENTTYPES_FIXTURE = OverrideContentTypesLayer()
TEST_USER_ADMIN = "adminmember1"
TEST_USER_1 = "simplemember1"
TEST_USER_2 = "simplemember2"
TEST_USER_3 = "simplemember3"
TEST_USER_4 = "simplemember4"
PASSWORD = "secret"

PROFILES = (
#    'Products.membrane:default',  # installed by the setuphandler
    'plone.app.versioningbehavior:default',
    'collective.mediaelementjs:default',
    'collective.memberdatatables:default',
    'collective.oembed:default',
    'collective.picturefill:default',
    'collective.requestaccess:default',
    'collective.transcode.star:default',
    'plone.app.dexterity:default',
    'plone.app.contenttypes:default',
    'dexterity.membrane:default',
    'collective.rcse:settings',
)

class Layer(PloneSandboxLayer):

    defaultBases = (
        mobile_testing.FIXTURE,
        event_testing.PAEventDX_FIXTURE,
        ptypes_testing.PLONE_APP_CONTENTTYPES_FIXTURE,
#        PLONE_APP_CONTENTTYPES_FIXTURE,

        twothumbs_testing.TWOTHUMBS_FIXTURE,

        etherpad_testing.FIXTURE,
        fav_testing.FIXTURE,
        font_testing.FIXTURE,
        history_testing.FIXTURE,
        ckeditor_testing.FIXTURE,
        datatables_testing.FIXTURE,
        polls_testing.FIXTURE,
        portlet_fav_testing.FIXTURE,
        portlet_users_testing.FIXTURE,
        readitlayer_testing.FIXTURE,
        themeswither_testing.FIXTURE,
        whathappened_testing.FIXTURE,
    )

    def setUpZope(self, app, configurationContext):
        import collective.rcse
        import dexterity.membrane
        import plone.app.dexterity
        import plone.app.versioningbehavior
        import plone.app.collection
        import plone.namedfile
        import collective.z3cform.html5widgets

        import collective.js.jqueryui
        import plone.app.versioningbehavior
        import five.localsitemanager
        import collective.indexing
        import Products.membrane
        import plone.app.contentrules

        self.loadZCML(package=dexterity.membrane)
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=plone.app.versioningbehavior)
        self.loadZCML(package=plone.app.collection)
        self.loadZCML(package=plone.namedfile)
        self.loadZCML(package=collective.z3cform.html5widgets)

        self.loadZCML(package=collective.js.jqueryui)
        self.loadZCML(package=plone.app.versioningbehavior)
        self.loadZCML(package=five.localsitemanager)
        self.loadZCML(package=collective.indexing)
        self.loadZCML(package=Products.membrane)
        self.loadZCML(package=plone.app.contentrules)
        z2.installProduct(app, 'Products.membrane')  # initialize
        self.loadZCML(package=collective.rcse)
        setupCoreSessions(app)

    def setUpPloneSite(self, portal):
        #make global request work
        from zope.globalrequest import setRequest
        setRequest(portal.REQUEST)

        #We apply profile of addon which has no testing layer here
        for profile in PROFILES:
            self.applyProfile(portal, profile)

        #portal.membrane_tool.user_adder = "rcse"
        #portal.membrane_tool.membrane_types.append("collective.rcse.member")
        #The setup unactivate source users to use CAS. because we are in test
        #we just reactivate sources users
        #portal.acl_users.source_users.manage_activateInterfaces([
        #    "IAuthenticationPlugin",
        #    "IUserAdderPlugin",
        #    "IUserEnumerationPlugin",
        #    "IUserIntrospection",
        #    "IUserManagement",
        #])

        self.regtool = getToolByName(portal, 'portal_registration')
        self.mtool = getToolByName(portal, 'membrane_tool')
        self.create_test_user(portal)
        key = 'collective.rcse.security.ISecuritySettings.addGroupPermission'
        portal.portal_registry[key] = "Member"

        login(portal, SITE_OWNER_NAME)
        self.create_user(portal, TEST_USER_ADMIN, function="Admin",
                         first_name="admin", last_name="rcse")
        setRoles(portal, TEST_USER_ADMIN, ["Member", "Site Administrator"])
        simplemember1 = self.create_user(portal, TEST_USER_1,
                         first_name="User", last_name="1")
        self.create_user(portal, TEST_USER_2,
                         first_name="User", last_name="2")
        self.create_company(portal, simplemember1)
        logout()
        transaction.commit()

    def create_test_user(self, portal):
        directory = portal.users_directory
        createContentInContainer(directory, 'collective.rcse.member',
                                 username=TEST_USER_NAME)
        createContentInContainer(directory, 'collective.rcse.member',
                                 username=SITE_OWNER_NAME)

    def create_user(self, portal, username,
                    role="Member", company='Company',
                    first_name="John", last_name="Doe",
                    email="no-reply@example.com", function="Function",
                    city="City", **kwargs):
        # https://pypi.python.org/pypi/plone.app.testing/4.2.2#id1
        # Create user content
        self.regtool.addMember(username, PASSWORD)
        # Update user content
        item = self.mtool(getUserName=username)[0].getObject()
        item.company_id=company
        item.company=company
        item.first_name=first_name
        item.last_name=last_name
        item.email=email
        item.function=function
        item.city=city
        for key, value in kwargs.items():
            setattr(item, key, value)
        self._renameUserContent(item)
        # Activate user
        wtool = getToolByName(portal, 'portal_workflow')
        wtool.doActionFor(item, 'approve')
        return item

    def _renameUserContent(self, item):
        directory = item.aq_inner.aq_parent
        title = '%s %s' % (item.first_name,
                           item.last_name)
        item.setTitle(title)
        new_id = INameChooser(directory).chooseName(title, item)
        self.mtool.unindexObject(item)
        directory.manage_renameObject(item.id, new_id)
        self.mtool.indexObject(item)

    def create_company(self, portal, user_item, corporate_name="Corporate name",
                       sector="Sector", postal_code="Postal code",
                       city="City", **kwargs):
        company_id = createCompany(user_item, getRequest())
        company = portal.companies_directory[company_id]
        company.corporate_name = corporate_name
        company.sector = sector
        company.postal_code = postal_code
        company.city = city
        for key, value in kwargs.items():
            setattr(company, key, value)


class SeleniumLayer(BaseLayer):
    defaultBases = (z2.ZSERVER_FIXTURE, )

    def testSetUp(self):
        # get info for start up the browser
        driver = os.environ.get('SELENIUM_DRIVER', '').lower() or 'firefox'
        webdriver = __import__(
            'selenium.webdriver.%s.webdriver' % driver, fromlist=['WebDriver'])
        args = [arg.strip() for arg in
                os.environ.get('SELENIUM_ARGS', '').split()
                if arg.strip()]
        self['browsers'] = []
        self['webdriver'] = webdriver
        self['driver'] = driver
        self['args'] = args
        self['getNewBrowser'] = self.getNewBrowser

    def getNewBrowser(self, url=None):
        browser = self['webdriver'].WebDriver(*self['args'])
        browser.implicitly_wait(10)  # zope/plone are quite slow
        self['browsers'].append(browser)
        if url is not None:
            browser.get(url)
        return browser

    def testTearDown(self):
        for browser in self['browsers']:
            browser.close()
            del browser

SELENIUM_FIXTURE = SeleniumLayer()

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
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="collective.rcse:Robot")

SELENIUM = FunctionalTesting(
    bases=(FIXTURE, SELENIUM_FIXTURE,),
    name="collective.rcse:Selenium"
)
