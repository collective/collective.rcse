from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles
#http://developer.plone.org/security/custom_permissions.html
security = ModuleSecurityInfo('collective.rcse')
perms = []

for typename in (
    "audio",
    "document",
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
    setDefaultRoles(permname, ('Manager',))

AddAudio = "collective.rcse: Add audio"
AddDocument = "collective.rcse: Add document"
AddEtherpad = "collective.rcse: Add etherpad"
AddEvent = "collective.rcse: Add event"
AddFile = "collective.rcse: Add file"
AddGroup = "collective.rcse: Add group"
AddImage = "collective.rcse: Add image"
AddVideo = "collective.rcse: Add video"

security.declarePublic('AddCompany')
setDefaultRoles('collective.rcse: Add company', ('Authenticated',))
AddCompany = "collective.rcse: Add company"
