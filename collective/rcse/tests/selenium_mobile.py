import time
import unittest

from collective.rcse import testing
import transaction
from selenium.common.exceptions import NoSuchElementException


def sleep(before=2, after=2):
    def decorator(f):
        def wrapper(*args, **kwargs):
            time.sleep(before)
            results = f(*args, **kwargs)
            time.sleep(after)
            return results
        return wrapper
    return decorator


class MobileTheme(unittest.TestCase):
    layer = testing.SELENIUM

    def setUp(self):
        super(MobileTheme, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        transaction.commit()

    def getNewBrowser(self, url=None):
        browser = self.layer['getNewBrowser'](url=url)
        browser.find_element_by_id('siteaction-themeswitcher_mobile').click()
        return browser

    @sleep()
    def login(self, browser, username, password, next_url=None):
        """Login a user and redirect to next_url"""
#        browser.get()
        browser.find_element_by_name("__ac_name").send_keys(username)
        browser.find_element_by_name("__ac_password").send_keys(password)
        browser.find_element_by_name('submit').click()
        if next_url:
            browser.get(next_url)

    @sleep()
    def open_add(self, browser, what=None, where=None):
        """Use the addbutton in RCSE header to get an add form"""
        pass

    @sleep()
    def do_create_group(self, browser, title, description=None, image=None):
        pass

    @sleep()
    def is_group(browser):
        css_class = browser.find_element_by_tag_name('body').get_attribute('class')
        return 'portaltype-collective-rcse-group' in css_class

    def open_group_manage(self, browser, action=None):
        pass

    @sleep()
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

    @sleep(before=0, after=1)
    def open_manage_portlet(self, browser):
        browser.get(browser.current_url + '/@@manage-portlets')

    @sleep(before=0)
    def open_add_portlet(self, browser, column, portlet, submit=False):
        """column in ("left", "right")
        """
        if not browser.current_url.endswith('/@@manage-portlets'):
            self.open_manage_portlet(browser)
        self.open_panel(browser, column)
        name = "portletmanager-plone-%scolumn" % column
        manager = browser.find_element_by_id(name)
        select = manager.find_element_by_tag_name("select")
        options = select.find_elements_by_tag_name("option")
        for option in options:
            if portlet in option.text:
                option.click()
                break
        if submit:
            browser.find_element_by_id('form.actions.save').click()

    def click_icon(self, browser, icon):
        selector = '[data-icon="%s"]' % icon
        browser.find_element_by_css_selector(selector).click()

    def open_panel(self, browser, side):
        if side == "left":
            self.click_icon(browser, "bars")
        elif side == "right":
            self.click_icon(browser, "grid")
        else:
            self.assertTrue(False, msg="Panel %s doesn't exists" % side)
