from collective.rcse.tests.selenium_desktop import DesktopTheme
from collective.rcse.tests.selenium_mobile import MobileTheme
from collective.rcse import testing
import unittest2 as unittest


class ScenarioTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_portlet_calendar(self):
        browser = self.getNewBrowser(self.portal_url)
        self.login(browser, testing.TEST_USER_ADMIN, testing.PASSWORD)
        self.open_add_portlet(browser, "left", "Calendar portlet", submit=True)
        browser.find_element_by_link_text("Return").click()
        self.open_panel(browser, "left")
        browser.quit()


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
    test_suite.addTest(unittest.makeSuite(MobileContentTypesTestCase))
    return test_suite
