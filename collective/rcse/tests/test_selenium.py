from collective.rcse.tests.selenium_desktop import DesktopTheme
from collective.rcse.tests.selenium_mobile import MobileTheme
from collective.rcse import testing
import unittest2 as unittest


class ScenarioTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_register(self):
        self.user = self.getNewBrowser(self.portal_url)
        self.register(self.user, 'toto', 'passs', email="toto@example.com",
                      first_name="Toto", last_name="Pass", function="tester",
                      company="The company", city="TotoLand")
        self.login(self.user, 'toto', 'passs')
        self.user.get(self.portal_url)
        self.assertIn('Your profile is waiting for approval',
                      self.user.page_source)

        self.admin = self.getNewBrowser(self.portal_url)
        self.login(self.admin, testing.TEST_USER_ADMIN, testing.PASSWORD)
        self.admin.get('%s/users_directory/@@users_manage_pending'
                       % self.portal_url)
        xpath = ('//table[@id="members-datatable"]//td[text()="toto"]/'
                 'parent::tr/td/form//input[@id="form-buttons-approve"]')
        self.admin.find_element_by_xpath(xpath).click()
        self.user.get(self.portal_url)
        self.assertIn('Please complete your company information',
                      self.user.page_source)

        self.edit_company(self.user, title="The company",
                         corporate_name="The company")
        self.assertIn('My profile', self.user.page_source)
        self.assertIn('News', self.user.page_source)

    def test_portlet_calendar(self):
        browser = self.getNewBrowser(self.portal_url)
        self.login(browser, testing.TEST_USER_ADMIN, testing.PASSWORD)
        self.open_add_portlet(browser, "left", "Calendar portlet", submit=True)
        browser.find_element_by_link_text("Return").click()
        self.open_panel(browser, "left")


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
