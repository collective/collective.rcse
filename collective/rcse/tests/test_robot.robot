*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  collective/history/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Assert: I can't browse the rcse without being logged-in
    Given I'm not loggedin
     When I'm on the mobile version
      And I'm on the home page
     Then I see the login form

    Given I'm not loggedin
          Import library  Dialogs
          Pause execution
     When I'm on the desktop version
      And I'm on the home page
     Then I see the login form

*** Keywords ***

I'm not loggedin
    Go to  ${PLONE_URL}/logout

I'm on the mobile version
    Click link  css=a#themeswitcher-mobile

I'm on the desktop version
    Click link  css=a#themeswitcher-desktop

I'm on the home page
    Go to  ${PLONE_URL}

I see the login form
    Element should be visible  css=#__ac_name
    Element should be visible  css=#__ac_password
