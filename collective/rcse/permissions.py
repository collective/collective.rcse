from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles

security = ModuleSecurityInfo('collective.rcse')
perms = []

for typename in (
    "audio",
    "document",
    "event",
    "file",
    "image",
    "video",
):
    ctype = "collective.rcse." + typename
    permid = 'Add' + typename.capitalize()
    permname = 'collective.rcse: Add ' + typename
    security.declarePublic(permid)
    setDefaultRoles(permid, ('Manager', ))

AddAudio = "collective.rcse: Add audio"
AddDocument = "collective.rcse: Add document"
AddEvent = "collective.rcse: Add event"
AddFile = "collective.rcse: Add file"
AddImage = "collective.rcse: Add image"
AddVideo = "collective.rcse: Add video"
