import time
import transaction
import unittest

from collective.rcse import testing


def sleep(before=2, after=2):
    def decorator(f):
        def wrapper(*args, **kwargs):
            time.sleep(before)
            results = f(*args, **kwargs)
            time.sleep(after)
            return results
        return wrapper
    return decorator


class DesktopTheme(unittest.TestCase):
    layer = testing.SELENIUM

    def setUp(self):
        super(DesktopTheme, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.getNewBrowser = self.layer['getNewBrowser']
        transaction.commit()

    @sleep(before=0, after=1)
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

    # User

    @sleep(before=0)
    def login(self, browser, username, password, next_url=None):
        """Login a user and redirect to next_url"""
        browser.get('%s/login' % self.portal_url)
        browser.find_element_by_name("__ac_name").send_keys(username)
        browser.find_element_by_name("__ac_password").send_keys(password)
        browser.find_element_by_name('submit').click()
        if next_url:
            browser.get(next_url)
        else:
            browser.find_element_by_id("content-core")\
                .find_element_by_tag_name("a").click()

    def logout(self, browser):
        browser.get('%s/logout' % self.portal_url)

    def register(self, browser, username, password, send=True,
                 email="no-reply@example.com", first_name="John",
                 last_name="Doe", function="Function", company="Company",
                 city="City"):
        self.logout(browser)
        browser.get('%s/@@register' % self.portal_url)
        browser.find_element_by_name("form.widgets.login").send_keys(username)
        browser.find_element_by_name("form.widgets.password").send_keys(password)
        browser.find_element_by_name("form.widgets.password_confirm").send_keys(password)
        self.register_info(browser, False, email, first_name, last_name,
                           function, company, city)
        if send:
            browser.find_element_by_name("form.buttons.register").click()

    def verify_user(self, browser, **kwargs):
        browser.get('%s/@@personal-information' % self.portal_url)
        #rcse redirect the user depends on what is the state of the current user
        if browser.current_url.endswith("@@register_information"):
            self.register_info(browser, **kwargs)
        if browser.current_url.endswith("edit"):
            self.edit_member(browser, **kwargs)

    def register_info(self, browser, send=True, email="no-reply@example.com",
                      first_name="John", last_name="Doe", function="Function",
                      company="Company", city="City"):
        browser.find_element_by_name("form.widgets.email").send_keys(email)
        browser.find_element_by_name("form.widgets.first_name").send_keys(first_name)
        browser.find_element_by_name("form.widgets.last_name").send_keys(last_name)
        browser.find_element_by_name("form.widgets.function").send_keys(function)
        browser.find_element_by_name("form.widgets.city").send_keys(city)
        rcompany = self._select2(browser, "form-widgets-company", company)
        if rcompany != company:
            self._select2(browser, "form-widgets-company", "Create a new company")
            browser.find_element_by_name("form.widgets.new_company").send_keys(company)
        if send:
            browser.find_element_by_name("form.buttons.submit").click()

    def edit_member(self, browser, send=True, email="no-reply@example.com",
                    first_name="John", last_name="Doe", function="Function",
                    company="Company", city="City"):
        browser.find_element_by_name("form.widgets.email").send_keys(email)
        browser.find_element_by_name("form.widgets.first_name").send_keys(first_name)
        browser.find_element_by_name("form.widgets.last_name").send_keys(last_name)
        browser.find_element_by_name("form.widgets.function").send_keys(function)
        browser.find_element_by_name("form.widgets.city").send_keys(city)
        browser.find_element_by_name("form.buttons.save").click()

    # Company

    def edit_company(self, browser, send=True, title="Company",
                     corporate_name="Corporate name", sector="Sector",
                     postal_code="Postal code", city="City"):
        browser.find_element_by_name("form.widgets.IBasic.title").clear()
        browser.find_element_by_name("form.widgets.IBasic.title").send_keys(title)
        browser.find_element_by_name("form.widgets.corporate_name").send_keys(corporate_name)
        browser.find_element_by_name("form.widgets.sector").send_keys(sector)
        browser.find_element_by_name("form.widgets.postal_code").send_keys(postal_code)
        browser.find_element_by_name("form.widgets.city").send_keys(city)
        browser.find_element_by_name("form.buttons.save").click()

    # Group

    def do_create_group(self, browser, title, description=None, image=None):
        self.open_add(browser, what='Group')
        title_id = 'form-widgets-IDublinCore-title'
        desc_id = 'form-widgets-IDublinCore-description'
        browser.find_element_by_id(title_id).send_keys(title)
        if description is not None:
            browser.find_element_by_id(desc_id).send_keys(description)
        browser.find_element_by_id('form-buttons-save').click()

    @sleep(after=0)
    def is_group(browser):
        css_class = browser.find_element_by_tag_name('body').get_attribute('class')
        return 'portaltype-collective-rcse-group' in css_class

    @sleep()
    def open_group_manage(self, browser, action=None):
        if not self.is_group(browser):
            raise ValueError("can manage group if current page is not on group")
        browser.find_element_by_link_text("Manage").click()
        time.sleep(1)
        if action is not None:
            browser.find_element_by_link_text(action).click()

    @sleep(after=0)
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

    # Utils

    @sleep()
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

    @sleep(before=0)
    def open_manage_portlet(self, browser):
        browser.get(browser.current_url + '/@@manage-portlets')

    @sleep(before=1)
    def open_add_portlet(self, browser, column, portlet, submit=False):
        """column in ("left", "right")
        """
        if not browser.current_url.endswith('/@@manage-portlets'):
            self.open_manage_portlet(browser)
            time.sleep(1)
        name = "portletmanager-plone-%scolumn" % column
        manager = browser.find_element_by_id(name)
        #find id of the select2
        s2 = manager.find_element_by_class_name('select2-container')
        id = s2.get_attribute('id').replace('s2id_', '')
        self._select2(browser, id, portlet)
        if submit:
            browser.find_element_by_id('form.actions.save').click()

    def click_icon(self, browser, icon):
        if not icon.startswith("icon-"):
            icon = "icon-%s" % icon
        icons = browser.find_elements_by_class_name(icon)
        found = False
        for icon in icons:
            if icon.is_displayed():
                icon.click()
                found = True
                break
        if not found:
            raise ValueError("icon %s not found in the current page" % icon)

    def open_panel(self, browser, side):
        pass

    def find_tiles(self, browser):
        return browser.find_elements_by_class_name("rcse_tile_wrapper")

    def find_tile_by_title(self, browser, title):
        contents = self.find_tiles(browser)
        css = '.tilecontent > h2'
        for content in contents:
            titles = content.find_elements_by_css_selector(css)
            for t in titles:
                if t.text == title:
                    return content

    def find_tile_by_author(self, browser, author):
        contents = self.find_tiles(browser)
        css = '[rel="author"]'
        for content in contents:
            authors = content.find_elements_by_css_selector(css)
            for t in authors:
                if t.text == author:
                    return content

    def find_tile_by_group(self, browser, group):
        contents = self.find_tiles(browser)
        css = 'a.group'
        for content in contents:
            authors = content.find_elements_by_css_selector(css)
            for t in authors:
                if t.text == group:
                    return content
