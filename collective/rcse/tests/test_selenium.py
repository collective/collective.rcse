from collective.rcse.tests.selenium_desktop import DesktopTheme
from collective.rcse.tests.selenium_mobile import MobileTheme
from collective.rcse import testing
import unittest2 as unittest


class ScenarioTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_register(self):
        user = self.getNewBrowser(self.portal_url)
        self.register(user, 'toto', 'passs', email="toto@example.com",
                      first_name="Toto", last_name="Pass", function="tester",
                      company="The company", city="TotoLand")
        self.login(user, 'toto', 'passs')
        user.get(self.portal_url)
        self.assertIn('Your profile is waiting for approval',
                      user.page_source)
        admin = self.getNewBrowser(self.portal_url)
        self.login(admin, testing.TEST_USER_ADMIN, testing.PASSWORD)
        admin.get('%s/users_directory/@@users_manage_pending'
                       % self.portal_url)
        if not self.is_mobile:
            xpath = ('//table[@id="members-datatable"]//td[text()="toto"]/'
                     'parent::tr/td/form//input[@id="form-buttons-approve"]')
        else:
            xpath = ('//div[@class="directory"]/ul/li/h2[text()="Toto Pass"]/'
                     'parent::li/form//input[@id="form-buttons-approve"]')
        admin.find_element_by_xpath(xpath).click()
        user.get(self.portal_url)
        self.assertIn('Please complete your company information',
                      user.page_source)
        self.edit_company(user, title="The company",
                         corporate_name="The company")
        self.assertIn('My profile', user.page_source)
        self.assertIn('News', user.page_source)

    def test_portlet_calendar(self):
        browser = self.getNewBrowser(self.portal_url)
        self.login(browser, testing.TEST_USER_ADMIN, testing.PASSWORD)
        self.open_add_portlet(browser, "left", "Calendar portlet", submit=True)
        browser.find_element_by_link_text("Return").click()
        self.open_panel(browser, "left")
        portlets = browser.find_elements_by_class_name("portletCalendar")
        self.assertEqual(len(portlets), 1)

    def test_disabled_member(self):
        user = self.getNewBrowser(self.portal_url)
        self.login(user, testing.TEST_USER_1, testing.PASSWORD)
        admin = self.getNewBrowser(self.portal_url)
        self.login(admin, testing.TEST_USER_ADMIN, testing.PASSWORD)
        admin.get('%s/users_directory/john-doe-1/'
                  'content_status_modify?workflow_action=disable'
                  % self.portal_url)
        admin.get('%s/users_directory/@@users_manage_disabled' % self.portal_url)


class DesktopContentTypesTestCase(ScenarioTestCase, DesktopTheme):
    is_mobile = False

    def setUp(self):
        DesktopTheme.setUp(self)
        ScenarioTestCase.setUp(self)


class MobileContentTypesTestCase(ScenarioTestCase, MobileTheme):
    is_mobile = True

    def setUp(self):
        MobileTheme.setUp(self)
        ScenarioTestCase.setUp(self)


def test_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(DesktopContentTypesTestCase))
    test_suite.addTest(unittest.makeSuite(MobileContentTypesTestCase))
    return test_suite
