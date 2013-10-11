import transaction
import unittest2 as unittest
from collective.rcse import testing
from plone.app.testing import (
    setRoles,
    TEST_USER_ID,
    TEST_USER_PASSWORD,
    logout
)


class UnitTestCase(unittest.TestCase):

    def setUp(self):
        pass


class IntegrationTestCase(unittest.TestCase):

    layer = testing.INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        logout()
        self.portal = self.layer['portal']


class FunctionalTestCase(IntegrationTestCase):

    layer = testing.FUNCTIONAL

    def setUp(self):
        #we must commit the transaction
        transaction.commit()
