from collective.rcse.tests.selenium_desktop import DesktopTheme
from collective.rcse.tests.selenium_mobile import MobileTheme
import unittest2 as unittest


class ScenarioTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_register(self):
        import pdb; pdb.set_trace()
        # self.register
        # self.login
        # self.verify_user
        # self.admin.approve_user

    #def test_add_group(self):
    #    self.open_add(self.users['simple1'], what="Group")


class DesktopContentTypesTestCase(ScenarioTestCase, DesktopTheme):

    def setUp(self):
        DesktopTheme.setUp(self)
        ScenarioTestCase.setUp(self)


class MobileContentTypesTestCase(ScenarioTestCase, MobileTheme):

    def setUp(self):
        MobileTheme.setUp(self)
        ScenarioTestCase.setUp(self)


def test_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(DesktopContentTypesTestCase))
#    test_suite.addTest(unittest.makeSuite(MobileContentTypesTestCase))
    return test_suite
