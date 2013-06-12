from zope import component
from zope import interface
from zope import schema
from plone.registry.interfaces import IRecordModifiedEvent
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout
from z3c.form import form

from collective.rcse import i18n

_ = i18n._


class ISecuritySettings(interface.Interface):
    """We handle permissions settings throw a control-panel for an high level
    overview of what can be done by who"""

    addGroupPermission = schema.Choice(
        title=_(u"Add group"),
        vocabulary="plone.app.vocabularies.Roles",
        default="Manager",
    )


@component.adapter(ISecuritySettings, IRecordModifiedEvent)
def handle_security_update(records, event):
    record = event.record
    site = component.hooks.getSite()
    if record.fieldName == 'addGroupPermission':
        newValue = event.newValue
        #first we control add portal content for the current role
        permission = "Add portal content"
        permission_settings = site.permission_settings(permission=permission)
        p_acquire = permission_settings[0]["acquire"]
        p_roles = permission_settings[0]["roles"]
        c_roles = []
        role_can_add = False
        for role in p_roles:
            if role["checked"] != "CHECKED":
                continue
            c_roles.append(role["name"])
            if role["name"] == newValue and role["checked"] != "CHECKED":
                role_can_add = True
        if not role_can_add:
            c_roles.append(newValue)
            site.manage_permission(
                permission,
                roles=c_roles,
                acquire=p_acquire
            )

        #next we add the corresponding permission
        permission = "collective.rcse: Add group"
        permission_settings = site.permission_settings(permission=permission)
        p_acquire = permission_settings[0]["acquire"]
        roles = ["Manager"]
        if newValue != "Manager":
            roles.append(newValue)
        site.manage_permission(permission, roles=roles, acquire=p_acquire)


class SecurityControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ISecuritySettings

SecurityControlPanelView = layout.wrap_form(
    SecurityControlPanelForm,
    ControlPanelFormWrapper
)
SecurityControlPanelView.label = _(u"RCSE Security settings")
