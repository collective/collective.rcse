from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles
#http://developer.plone.org/security/custom_permissions.html
security = ModuleSecurityInfo('collective.rcse')
TYPE_ROLES = ('Manager', 'Site Administrator', 'Owner')
perms = []

for typename in (
    "article",
    "audio",
    "discussion",
    "etherpad",
    "event",
    "file",
    "group",
    "image",
    "video",
):
    ctype = "collective.rcse." + typename
    permid = 'Add' + typename.capitalize()
    permname = 'collective.rcse: Add ' + typename
    security.declarePublic(permid)
    setDefaultRoles(permname, TYPE_ROLES)

AddArticle = "collective.rcse: Add article"
AddAudio = "collective.rcse: Add audio"
AddDiscussion = "collective.rcse: Add discussion"
AddEtherpad = "collective.rcse: Add etherpad"
AddEvent = "collective.rcse: Add event"
AddFile = "collective.rcse: Add file"
AddGroup = "collective.rcse: Add group"
AddImage = "collective.rcse: Add image"
AddVideo = "collective.rcse: Add video"

security.declarePublic('AddCompany')
setDefaultRoles('collective.rcse: Add company', ('Manager', 'Authenticated',))
AddCompany = "collective.rcse: Add company"

security.declarePublic('AddPoxyGroup')
setDefaultRoles('collective.rcse: Add proxy group', ('Manager',))
AddCompany = "collective.rcse: Add proxy group"

security.declarePublic('MakePrivate')
MakePrivate = "collective.rcse: Make private"
setDefaultRoles(MakePrivate, TYPE_ROLES)

security.declarePublic('MakePublishedInternally')
MakePublishedInternally = "collective.rcse: Make published internally"
setDefaultRoles(MakePublishedInternally, TYPE_ROLES)

security = ModuleSecurityInfo('collective.requestaccess')

security.declarePublic('AddRequest')
AddRequest = 'collective.requestaccess: Add request'
setDefaultRoles(AddRequest, ('Member', 'Manager'))

security.declarePublic('ReviewRequest')
ReviewRequest = 'collective.requestaccess: Review request'
setDefaultRoles(ReviewRequest, ('Manager', 'Site Administrator', 'Owner'))

security.declarePublic('AddXItemsPortlet')
AddXItemsPortlet = 'collective.rcse: Add xitems portlet'
setDefaultRoles(AddXItemsPortlet,
                ('Manager', 'Site Administrator', 'Owner',))
