import time
import unittest

from collective.rcse import testing
import transaction

def sleep(f):
    def wrapper(*args):
        time.sleep(2)
        results = f(*args)
        time.sleep(2)
        return results
    return wrapper


class DesktopTheme(unittest.TestCase):
    layer = testing.SELENIUM

    def setUp(self):
        super(DesktopTheme, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.getNewBrowser = self.layer['getNewBrowser']
        transaction.commit()

        self.user1 = self.getNewBrowser(self.portal_url)
        self.login(self.user1, "simplemember1", "secret")
        self.verify_user(self.user1, "simplemember1")
        self.user2 = self.getNewBrowser(self.portal_url)
        self.login(self.user2, "simplemember2", "secret")
        self.verify_user(self.user2, "simplemember1")

    @sleep
    def _select2(self, browser, byid, value):
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
                return value

        select2.find_element_by_tag_name("a").click()
        return select2.find_element_by_class_name('select2-chosen').text

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
        browser.find_element_by_id('addbutton').find_element_by_tag_name('a').click()
        time.sleep(1)
        if what is not None:
            rwhat = self._select2(browser, 'form-widgets-what', what)
            self.assertEqual(rwhat, what)
        if where is not None:
            rwhere = self._select2(browser, 'form-widgets-where', where)
            self.assertEqual(rwhere, where)
        browser.find_element_by_id("rcseaddform").find_element_by_class_name('btn-primary').click()

    def do_create_group(self, browser, title, description=None, image=None):
        self.open_add(browser, what='Group')
        title_id = 'form-widgets-IDublinCore-title'
        desc_id = 'form-widgets-IDublinCore-description'
        browser.find_element_by_id(title_id).send_keys(title)
        if description is not None:
            browser.find_element_by_id(desc_id).send_keys(description)
        browser.find_element_by_id('form-buttons-save').click()

    @sleep
    def is_group(browser):
        css_class = browser.find_element_by_tag_name('body').get_attribute('class')
        return 'portaltype-collective-rcse-group' in css_class

    @sleep
    def open_group_manage(self, browser, action=None):
        if not self.is_group(browser):
            raise ValueError("can manage group if current page is not on group")
        
        browser.find_element_by_link_text("Manage").click()
        time.sleep(1)
        if action is not None:
            browser.find_element_by_link_text(action).click()

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
        self._select2(browser, 'form-widgets-userid', who)
        self._select2(browser, 'form-widgets-role', role)
        browser.find_element_by_link_text('Propose an access').click()

    def missing_info(self, browser, email, first_name, last_name, function, 
                     department):
    
        browser.find_element_by_name("form.widgets.email").send_keys(email)
        browser.find_element_by_name("form.widgets.first_name").send_keys(first_name)
        browser.find_element_by_name("form.widgets.last_name").send_keys(last_name)

        browser.find_element_by_name("form.widgets.function").send_keys(function)

        browser.find_element_by_name("form.buttons.save").click()

    def register_info(self, browser, email, first_name, last_name, function,
                       department, company):
    
        browser.find_element_by_name("form.widgets.email").send_keys(email)
        browser.find_element_by_name("form.widgets.first_name").send_keys(first_name)
        browser.find_element_by_name("form.widgets.last_name").send_keys(last_name)
        browser.find_element_by_name("form.widgets.function").send_keys(function)

        rcompany = self._select2(browser, "form-widgets-company", company)
        if rcompany != company:
            self._select2(browser, "form-widgets-company", "Create a new company")
            browser.find_element_by_name("form.widgets.new_company").send_keys(company)

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
            self.register_info(browser, email, first_name, last_name, function,
                       department, company)
        if browser.current_url.endswith("edit"):
            self.missing_info(browser, email, first_name, last_name, function,
                         department)
