from collective.rcse.tests.selenium_desktop import DesktopTheme
from collective.rcse.tests.selenium_mobile import MobileTheme
from collective.rcse import testing
import unittest2 as unittest


class ScenarioTestCase(unittest.TestCase):

    def test_owner_can_delete_its_group(self):
        user = self.getNewBrowser(self.portal_url)
        self.login(user, testing.TEST_USER_1, testing.PASSWORD)
        self.do_create_group(user, 'group of user 1')
        self.open_group_manage(user, action="Delete")
        user.find_element_by_id("form-buttons-delete").click()
        self.assertEqual(user.current_url, self.portal_url + '/home')
        user.close()


class DesktopSecurityTestCase(ScenarioTestCase, DesktopTheme):
    is_mobile = False

    def setUp(self):
        DesktopTheme.setUp(self)
        ScenarioTestCase.setUp(self)


class MobileSecurityTestCase(ScenarioTestCase, MobileTheme):
    is_mobile = True

    def setUp(self):
        MobileTheme.setUp(self)
        ScenarioTestCase.setUp(self)


def test_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(DesktopSecurityTestCase))
    test_suite.addTest(unittest.makeSuite(MobileSecurityTestCase))
    return test_suite
