from plone.app.testing import (
    PloneWithPackageLayer,
    IntegrationTesting,
    FunctionalTesting,
)
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.testing import z2
import collective.requestaccess
from plone.app.testing.helpers import setRoles
from plone.app.testing.interfaces import TEST_USER_ID


class MyLayer(PloneWithPackageLayer):
    def setUpPloneSite(self, portal):
        super(MyLayer, self).setUpPloneSite(portal)
        #create one member + one site administrator
        acl_users = portal.acl_users
        acl_users.userFolderAddUser("tmember", "secret", ['Member'], [])
        saroles = ['Member', 'Site Administrator']
        acl_users.userFolderAddUser("tsiteadmin", "secret", saroles, [])
        setRoles(portal, TEST_USER_ID, ["Manager"])
        portal.invokeFactory('Folder', 'test-folder')
        portal.invokeFactory('Document', 'test-document')
        setRoles(portal, TEST_USER_ID, ["Member"])


FIXTURE = MyLayer(
    zcml_filename="configure.zcml",
    zcml_package=collective.requestaccess,
    additional_z2_products=[],
    gs_profile_id='collective.requestaccess:default',
    name="collective.requestaccess:FIXTURE"
)

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="collective.requestaccess:Integration"
)

FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,),
    name="collective.requestaccess:Functional"
)

ROBOT = FunctionalTesting(
    bases=(AUTOLOGIN_LIBRARY_FIXTURE, FIXTURE, z2.ZSERVER),
    name="collective.requestaccess:Robot"
)
