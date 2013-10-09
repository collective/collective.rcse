import unittest

from collective.rcse import testing
import transaction


class SeleniumTestCase(unittest.TestCase):
    layer = testing.SELENIUM

    def setUp(self):
        super(SeleniumTestCase, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.getNewBrowser = self.layer['getNewBrowser']
        transaction.commit()

    def is_mobile(self, browser):
        """test if the current opened page is on the mobile theme"""
        return False

    def select2(self, browser, byid, value):
        """when you use select2, you have to use id.
        if select id was "form-widgets-function"
        it becomes "s2id_form-widgets-function"
        """
        newid = "s2id_" + byid
        select2 = browser.find_element_by_id(newid)
        select2.find_element_by_tag_name("a").click()
        options = browser.find_elements_by_class_name("select2-result")
        for option in options:
            if option.text == value:
                option.click()
                break
        time.sleep(1)

    def login(self, browser, username, password, next_url=None):
        """Login a user and redirect to next_url"""
#        browser.get()
        browser.find_element_by_name("__ac_name").send_keys(username)
        browser.find_element_by_name("__ac_password").send_keys(password)
        browser.find_element_by_name('submit').click()
        if next_url:
            browser.get(next_url)

    def open_add(self, browser, what=None, where=None):
        """Use the addbutton in RCSE header to get an add form"""
        browser.find_element_by_id('addbutton').find_element_by_tag_name('a').click()
        time.sleep(1)
        if what is not None:
            self.select2(browser, 'form-widgets-what', what)
        if where is not None:
            self.select2(browser, 'form-widgets-where', where)
        browser.find_element_by_id("rcseaddform").find_element_by_class_name('btn-primary').click()

    def do_create_group(self, browser, title, description=None, image=None):
        if self.is_mobile(browser):
            pass
        else:
            self.add(browser, what='Groupe')
            title_id = 'form-widgets-IDublinCore-title'
            desc_id = 'form-widgets-IDublinCore-description'
            browser.find_element_by_id(title_id).send_keys(title)
            if description is not None:
                browser.find_element_by_id(desc_id).send_keys(description)
            browser.find_element_by_id('form-buttons-save').click()

    def is_group(browser):
        time.sleep(1)
        css_class = browser.find_element_by_tag_name('body').get_attribute('class')
        return 'portaltype-collective-rcse-group' in css_class

    def open_group_manage(self, browser, action=None):
        time.sleep(1)
        if not self.is_group(browser):
            raise ValueError("can manage group if current page is not on group")
        if self.is_mobile(browser):
            pass
        else:
            browser.find_element_by_link_text("Manage").click()
            time.sleep(1)
            if action is not None:
                browser.find_element_by_link_text(action).click()

    def assertGroupState(self, browser, state):
        """verify state of the current group"""
        time.sleep(1)
        if not self.is_group(browser):
            raise ValueError("can manage group if current page is not on group")
        if self.is_mobile(browser):
            pass
        else:
            if not browser.current_url.endswith('/group_status'):
                self.open_group_manage(browser, action="Etat")
            button = browser.find_element_by_link_text("Make %s" % state)
            return button.get_attribute("disabled") == 'true'

    def set_group_state(self, browser, action):
        """Make private, Make moderated, Make open"""
        if not self.is_group(browser):
            raise ValueError("can manage group if current page is not on group")
        if self.is_mobile(browser):
            pass
        else:
            if not browser.current_url.endswith('/group_status'):
                self.open_group_manage(browser, action="Etat")
            browser.find_element_by_link_text(action).click()

    def add_group_invite(self, browser, who, role):
        if not self.is_group(browser):
            raise ValueError("can manage group if current page is not on group")
        if self.is_mobile(browser):
            pass
        else:
            if not browser.current_url.endswith('/group_status'):
                self.open_group_manage(browser, action="Inviter un utilisateur")
            self.select2(browser, 'form-widgets-userid', who)
            self.select2(browser, 'form-widgets-role', role)
            browser.find_element_by_link_text('Propose an access').click()


class ContentTypes(SeleniumTestCase):
    def setUp(self):
        super(ContentTypes, self).setUp()
        self.user1 = self.getNewBrowser(self.portal_url)
        self.user2 = self.getNewBrowser(self.portal_url)
#        self.user3 = self.getNewBrowser(self.portal_url)
#        self.user4 = self.getNewBrowser(self.portal_url)

    def test_create_group(self):
        import pdb;pdb.set_trace()
        self.login(self.user1, "simplemember1", "secret")
        self.login(self.user1, "simplemember2", "secret")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
