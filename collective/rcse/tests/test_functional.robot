*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  collective/history/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Check I can logged in
    Log in as site owner
    Go to homepage
    Add dexterity    collective.rcse.group    My group
    Wait Until Page Contains Element    css=body.section-my-group
    Go to history
    Verify history    1   created       /my-group

*** Keywords ***

Add dexterity
    [Arguments]  ${id}  ${title}
    Go to  ${PLONE_URL}/++add++${id}
    Wait Until Page Contains Element  css=#form-widgets-IDublinCore-title
    Input Text  css=#form-widgets-IDublinCore-title  ${title}
    Click Button  Save
