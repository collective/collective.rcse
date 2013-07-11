*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plonetheme/jquerymobile/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Assert: Let's go for a long story

    Given I switch to 'mobile'
      And Fix weird setup issues
     When I set security settings to let member add groups
     Then I login as 'simplemember1'
      And I add 'group' 'Group of Simple Member 1'
      And I invite member 'simplemember3' to become 'Contributor'
      And I add document 'My first document'

    #Now check a member can request access as contributor
    Given I login as 'simplemember2'
     When I go to section 'Group of Simple Member 1'
      And I request access 'Contributor'
      And I login as 'simplemember1'
      And I go to section 'Group of Simple Member 1'
      And I go to document action 'review_requests'
      And I validate the request
      And I login as 'simplemember2'
      And I go to section 'Group of Simple Member 1'
     Then I add document 'I can work for you now'

    #Now check invited member can join the party
    Given I login as 'simplemember3'
     When I go to personal 'personaltools-my_requests'
      And I validate the invitation

Assert: I can't browse the rcse without being logged-in
    Given I logout
      And I switch to 'mobile'
      And I go to section 'Home'
     Then I see the login form

*** Keywords ***

#LOGIN / LOGOUT
I logout
    Go to  ${PLONE_URL}/logout

I login as '${username}'
    I logout
    Go to  ${PLONE_URL}/login
    Log in  ${username}  ${TEST_USER_PASSWORD}
    Go to  ${PLONE_URL}

I switch to '${themeversion}'
    Click link  css=a[title='themeswitcher_${themeversion}']


#MENU
I open the add content menu
    JQMobile:Open left panel
    Wait Until Page Contains Element  css=#plone-contentmenu-factories a
    Click Link  css=#plone-contentmenu-factories a

#LOCATIONS
I go to section '${title}'
    Click Link  css=a#globalsections
    Wait Until Page Contains Element  css=#popup-globalsections
    Click Link  ${title}

I go to personal '${action}'
    Click Link  css=a#personalbar
    Wait Until Page Contains Element  css=#popup-personalbar
    Click Link  ${action}

I go to document action '${action}'
    Click Link  css=#${action}

#ACTIONS
I request access '${role}'
    Click Link  css=#add_request_access
    Select From List  css=#form-widgets-role  ${role}
    Click button  Request access
    Element Should Contain  css=.portalMessage  Your request has been saved

I invite member '${memberid}' to become '${role}'
    Click Link  css=#add_invite_access
    Select From List  css=#form-widgets-userid  ${memberid}
    Select From List  css=#form-widgets-role  ${role}
    Import library  Dialogs
    Pause execution

    Click button  Propose access
    Element Should Contain  css=.portalMessage  Your request has been saved

I validate the request
    Click button  Validate access

I validate the invitation
    Click button  Validate access

I set security settings to let member add groups
    Go to  ${PLONE_URL}/@@rcse-security-controlpanel
    Select From List  css=#form-widgets-addGroupPermission  Member
    Click button  name=form.buttons.save

I add '${rcsetypeid}' '${title}'
    I open the add content menu
    Click link  css=a#collective-rcse-${rcsetypeid}
    Wait Until Page Contains Element  css=#form-widgets-IDublinCore-title
    Input Text  form-widgets-IDublinCore-title  ${title}
    Click button  name=form.buttons.save
    I see status message 'Item created'

I add document '${title}'
    I open the add content menu
    Click link  css=a#collective-rcse-document
    Wait Until Page Contains Element  css=#form-widgets-IDublinCore-title
    Input Text  form-widgets-IDublinCore-title  ${title}
    Click Element  css=div[contenteditable='true']
    Input Text  css=div[contenteditable='true']  hello world
    Import library  Dialogs
    Pause execution
    
    Click button  name=form.buttons.save
    I see status message 'Item created'

#ASSERTIONS
I can't add a group
    JQMobile:Open left panel
    Page Should Not Contain  css=#plone-contentmenu-factories a

I see status message '${message}'
    Element Text Should Be  css=.portalMessage  ${message}

I see the login form
    Element should be visible  css=#__ac_name
    Element should be visible  css=#__ac_password

Fix weird setup issues
    I login as 'simplemember1'
    I login as 'simplemember2'
    I login as 'simplemember3'
    I login as 'siteadmin'
    I login as '${SITE_OWNER_NAME}'
