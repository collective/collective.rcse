import transaction
import unittest2 as unittest
from plone.app.testing import (
    setRoles,
    TEST_USER_ID,
)
from collective.requestaccess import testing


class UnitTestCase(unittest.TestCase):

    def setUp(self):
        pass


class IntegrationTestCase(unittest.TestCase):

    layer = testing.INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']
        self.login('Member')

    def login(self, role):
        setRoles(self.portal, TEST_USER_ID, [role])


class FunctionalTestCase(IntegrationTestCase):

    layer = testing.FUNCTIONAL

    def setUp(self):
        #we must commit the transaction
        transaction.commit()
