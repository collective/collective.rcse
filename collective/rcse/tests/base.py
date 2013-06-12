import transaction
import unittest2 as unittest
from collective.rcse import testing
from plone.app.testing import (
    setRoles,
    TEST_USER_ID,
)


class UnitTestCase(unittest.TestCase):

    def setUp(self):
        pass


class IntegrationTestCase(unittest.TestCase):

    layer = testing.INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']
        self.login('Manager')
        self.portal.invokeFactory('Folder', 'test-folder')
        self.login('Member')
        self.folder = self.portal['test-folder']

    def login(self, role):
        setRoles(self.portal, TEST_USER_ID, [role])


class FunctionalTestCase(IntegrationTestCase):

    layer = testing.FUNCTIONAL

    def setUp(self):
        #we must commit the transaction
        transaction.commit()
