import time
import unittest2 as unittest

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

from collective.rcse.tests.selenium_desktop import DesktopTheme
from collective.rcse.tests.selenium_mobile import MobileTheme
from collective.rcse import testing


class ScenarioTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def _assertStatus(self, browser, message):
        """Looks for message in all status"""
        ok = False
        while not ok:
            try:
                status = browser.find_elements_by_class_name('portalMessage')
                text = ''.join([a.text for a in status])
                ok = True
            except StaleElementReferenceException:
                time.sleep(1)
        self.assertIn(message, text)

    def test_notification(self):
        user1 = self.getNewBrowser(self.portal_url)
        self.login(user1, testing.TEST_USER_1, testing.PASSWORD)
        user2 = self.getNewBrowser(self.portal_url)
        self.login(user2, testing.TEST_USER_2, testing.PASSWORD)
        user2.get('%s/home/companys-public-group' % self.portal_url)
        if self.is_mobile:
            group_header2 = user2.find_element_by_class_name(
                'description-wrapper'
                )
        else:
            group_header2 = user2.find_element_by_id('group-header')
        group_header2.find_element_by_id('cioppino_twothumbs_like').click()
        user1.get('%s/home/companys-public-group' % self.portal_url)
        if self.is_mobile:
            group_header = user1.\
                find_element_by_class_name('description-wrapper')
            button = group_header.find_element_by_xpath(
                'self::*//*[@data-rel="popup"]'
                )
            button.click()
            href = button.get_attribute('href')
            href = href[(href.rfind('/') + 2):]
            group_header = user1.find_element_by_id(href)
        else:
            group_header = user1.find_element_by_id('group-header')
            group_header.find_element_by_class_name('dropdown-toggle').click()
        group_header.find_element_by_id(
            'collective_whathappened_subscribe'
            ).click()
        group_header2.find_element_by_id('favoriting_add').click()
        user1.get(self.portal_url)
        count = user1.find_element_by_id('notifications-count').text
        self.assertEqual(count, u'1', 'Notifications count is not right')
        if self.is_mobile:
            user1.find_element_by_id('notifications').click()
            time.sleep(1)
            notification = user1.find_element_by_xpath(
                '//*[@id="popup-notifications"]/ul/li[1]//a').text
        else:
            user1.find_element_by_xpath('//*[@id="notifications"]/a').click()
            time.sleep(1)
            notification = user1.find_element_by_xpath(
                '//*[@id="notifications"]/ul/li[1]/a'
                ).text
        self.assertEqual(notification,
                         u'User 2 has added Company\'s '
                         u'public group to his favorites')
        user1.get('%s/@@collective_whathappened_notifications_all'
                  % self.portal_url)
        content = user1.find_element_by_id('content').text
        self.assertIn(notification, content,
                      'Notification not in all notifications')
        user1.get('%s/home/companys-public-group' % self.portal_url)
        self.assertRaises(NoSuchElementException, user1.find_element_by_id,
                          'notifications-count')

    def test_register(self):
        user = self.getNewBrowser(self.portal_url)
        self.register(user, 'toto', 'passs', email="toto@example.com",
                      first_name="Toto", last_name="Pass", function="tester",
                      company="The company", city="TotoLand")
        self.login(user, 'toto', 'passs')
        user.get(self.portal_url)
        self._assertStatus(user, 'Your profile is waiting for approval')
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
        self._assertStatus(user, 'Please complete your company information')
        self.edit_company(user, title="The company",
                          corporate_name="The company")
        user.get(self.portal_url)
        if self.is_mobile:
            user.find_element_by_id('addbutton-wrapper')
        else:
            headers = user.find_elements_by_class_name('documentFirstHeading')
            self.assertIn('My profile', headers[0].text)
            self.assertIn('News', headers[1].text)

    def test_disabled_member(self):
        user = self.getNewBrowser(self.portal_url)
        self.login(user, testing.TEST_USER_1, testing.PASSWORD)
        admin = self.getNewBrowser(self.portal_url)
        self.login(admin, testing.TEST_USER_ADMIN, testing.PASSWORD)
        admin.get('%s/users_directory/user-1/'
                  'content_status_modify?workflow_action=disable'
                  % self.portal_url)
        user.get(self.portal_url)
        self._assertStatus(user, 'Your profile has been disabled.')
        admin.get('%s/users_directory/@@users_manage_disabled'
                  % self.portal_url)
        if not self.is_mobile:
            xpath = ('//table[@id="members-datatable"]//'
                     'td[text()="simplemember1"]/'
                     'parent::tr/td/form//input[@id="form-buttons-enable"]')
        else:
            xpath = ('//div[@class="directory"]/ul/li/h2[text()="User 1"]/'
                     'parent::li/form//input[@id="form-buttons-enable"]')
        admin.find_element_by_xpath(xpath).click()
        user.get(self.portal_url)
        self.assertEqual(user.current_url, '%s/home' % self.portal_url)

    def test_portlet_calendar(self):
        browser = self.getNewBrowser(self.portal_url)
        self.login(browser, testing.TEST_USER_ADMIN, testing.PASSWORD)
        browser.get(self.portal_url)
        self.open_add_portlet(browser, "left", "Calendar portlet", submit=True)
        if self.is_mobile:
            self.click_icon(browser, 'circle-arrow-left')
        else:
            browser.find_element_by_link_text("Return").click()
        self.open_panel(browser, "left")
        portlets = browser.find_elements_by_class_name("portletCalendar")
        self.assertEqual(len(portlets), 1)
        browser.close()

    def test_comments(self):
        browser = self.getNewBrowser(self.portal_url)
        self.login(browser, testing.TEST_USER_ADMIN, testing.PASSWORD)
        self.do_create_group(browser, 'group for comments')
        self.open_add(browser, what="Article", where="group for comments")
        title_id = 'form-widgets-IDublinCore-title'
        title = "Please commenting me"
        browser.find_element_by_id(title_id).send_keys(title)
        browser.find_element_by_id('form-buttons-save').click()
        tile = self.find_tile_by_title(browser, title)
        self.assertIsNotNone(tile)
        self.click_icon(tile, "comments-alt")
        tile.find_element_by_tag_name("textarea").send_keys("coucou")
        tile.find_element_by_id("form-buttons-comment").click()
        comments = tile.find_elements_by_class_name("commentBody")
        comments = [comment.text for comment in comments]
        self.assertIn("coucou\nDelete", comments)
        browser.close()


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
