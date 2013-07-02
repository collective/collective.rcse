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

Assert: Let's go for a long story

    Given I'm loggedin as 'simplemember1'
      And I'm on the mobile version
      And I'm on the home page
     When I'm adding the group 'Group of Simple Member 1'
     Then I'm in the group 'Group of Simple Member 1'


*** Keywords ***

#LOGIN / LOGOUT
I'm not loggedin
    Go to  ${PLONE_URL}/logout

I'm loggedin as a '${USERNAME}'
    Go to  ${PLONE_URL}/login
    Log in  ${USERNALE}  ${TEST_USER_PASSWORD}

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

#ACTIONS
I'm adding the group '${title}'
    I open the add content menu
    Click link  css=a#${collective-rcse-group}
    Page should contain element  __ac_name
    Input Text  title  ${title}
    Import library  Dialogs
    Pause execution
    Click button  name=form.button.save
    Page Should Contain  Changes saved.

#ASSERTIONS
I see the login form
    Element should be visible  css=#__ac_name
    Element should be visible  css=#__ac_password
