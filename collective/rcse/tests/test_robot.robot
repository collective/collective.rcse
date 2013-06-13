*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plonetheme/jquerymobile/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Assert: I can't browse the rcse without being logged-in
    Given I'm not loggedin
      And I'm on the mobile version
      And I'm on the home page
     Then I see the login form

    Given I'm not loggedin
      And I'm on the desktop version
      And I'm on the home page
     Then I see the login form

Assert: Administrator can add groups
    Given I'm loggedin as the site owner
      And I'm on the mobile version
      And I'm on the home page
     When I open the add content menu
     Then I see 'collective-rcse-group' in the content menu

*** Keywords ***

#LOGIN / LOGOUT
I'm not loggedin
    Go to  ${PLONE_URL}/logout

I'm loggedin as a test user
    Log in as test user

I'm loggedin as the site owner
    Log in as site owner

#THEME SWITCHER
I'm on the mobile version
    Click link  css=li#siteaction-themeswitcher_mobile a

I'm on the desktop version
    Click link  css=a#siteaction-themeswitcher_desktop

#MENU
I open the add content menu
    JQMobile:Open left panel
    Click Link  css=#plone-contentmenu-factories a

#LOCATIONS
I'm on the home page
    Go to  ${PLONE_URL}

#ASSERTIONS
I see the login form
    Element should be visible  css=#__ac_name
    Element should be visible  css=#__ac_password

I see '${type}' in the content menu
    Element should be visible  css=a#${type}
