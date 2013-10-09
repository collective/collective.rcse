import time
import unittest

from collective.rcse import testing
import transaction
from selenium.common.exceptions import NoSuchElementException

def sleep(f):
    def wrapper(*args):
        time.sleep(2)
        results = f(*args)
        time.sleep(2)
        return results
    return wrapper

class MobileTheme(unittest.TestCase):
    layer = testing.SELENIUM

    def setUp(self):
        super(MobileTheme, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.getNewBrowser = self.layer['getNewBrowser']
        transaction.commit()

        self.user1 = self.getNewBrowser(self.portal_url)
        self.user1.find_element_by_id('siteaction-themeswitcher_mobile').click()
        self.login(self.user1, "simplemember1", "secret")
        self.verify_user(self.user1, "simplemember1")
        self.user2 = self.getNewBrowser(self.portal_url)
        self.user2.find_element_by_id('siteaction-themeswitcher_mobile').click()
        self.login(self.user2, "simplemember2", "secret")
        self.verify_user(self.user2, "simplemember2")

    @sleep
    def login(self, browser, username, password, next_url=None):
        """Login a user and redirect to next_url"""
#        browser.get()
        browser.find_element_by_name("__ac_name").send_keys(username)
        browser.find_element_by_name("__ac_password").send_keys(password)
        browser.find_element_by_name('submit').click()
        if next_url:
            browser.get(next_url)

    @sleep
    def open_add(self, browser, what=None, where=None):
        """Use the addbutton in RCSE header to get an add form"""
        pass

    @sleep
    def do_create_group(self, browser, title, description=None, image=None):
        pass

    @sleep
    def is_group(browser):
        css_class = browser.find_element_by_tag_name('body').get_attribute('class')
        return 'portaltype-collective-rcse-group' in css_class

    def open_group_manage(self, browser, action=None):
        pass

    @sleep
    def assertGroupState(self, browser, state):
        """verify state of the current group"""
        if not self.is_group(browser):
            raise ValueError("can manage group if current page is not on group")
        
        if not browser.current_url.endswith('/group_status'):
            self.open_group_manage(browser, action="Etat")
        button = browser.find_element_by_link_text("Make %s" % state)
        return button.get_attribute("disabled") == 'true'

    def set_group_state(self, browser, action):
        """Make private, Make moderated, Make open"""
        if not self.is_group(browser):
            raise ValueError("can manage group if current page is not on group")
        
        if not browser.current_url.endswith('/group_status'):
            self.open_group_manage(browser, action="Etat")
        browser.find_element_by_link_text(action).click()

    def add_group_invite(self, browser, who, role):
        if not self.is_group(browser):
            raise ValueError("can manage group if current page is not on group")
        
        if not browser.current_url.endswith('/group_status'):
            self.open_group_manage(browser, action="Inviter un utilisateur")
#        self.select2(browser, 'form-widgets-userid', who)
#        self.select2(browser, 'form-widgets-role', role)
        browser.find_element_by_link_text('Propose an access').click()

    def missing_info(self, browser, email, first_name, last_name, function):
    
        browser.find_element_by_name("form.widgets.email").send_keys(email)
        browser.find_element_by_name("form.widgets.first_name").send_keys(first_name)
        browser.find_element_by_name("form.widgets.last_name").send_keys(last_name)

        browser.find_element_by_name("form.widgets.function").send_keys(function)

        browser.find_element_by_name("form.buttons.save").click()

    def register_info(self, browser, email, first_name, last_name, function, company):
    
        browser.find_element_by_name("form.widgets.email").send_keys(email)
        browser.find_element_by_name("form.widgets.first_name").send_keys(first_name)
        browser.find_element_by_name("form.widgets.last_name").send_keys(last_name)
        browser.find_element_by_name("form.widgets.function").send_keys(function)

        browser.find_element_by_name("form.buttons.submit").click()

    def verify_user(self, browser, username):
        email = "jmf+adria%s@makina-corpus.com" % username
        email = email.replace(" ", "")
        first_name = "test"
        last_name = username
        function = "Achats"
        department = "Loire Atlantique"
        company = "Makina Corpus"

        #rcse redirect the user depends on what is the state of the current user
        if browser.current_url.endswith("@@register_information"):
            self.register_info(browser, email, first_name, last_name, function, company)
        if browser.current_url.endswith("edit"):
            self.missing_info(browser, email, first_name, last_name, function)
