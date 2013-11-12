from plone.app.z3cform import layout
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser import BrowserView
from z3c.form import button
from z3c.form import form
from zope import component
from zope import interface

from collective.rcse.i18n import _


class RebuildMembraneCatalogFormSchema(model.Schema):
    pass


class RebuildMembraneCatalogFormAdapter(object):
    interface.implements(RebuildMembraneCatalogFormSchema)
    component.adapts(interface.Interface)
    def __init__(self, context):
        self.context = context


class RebuildMembraneCatalogForm(AutoExtensibleForm, form.Form):
    schema = RebuildMembraneCatalogFormSchema
    enableCSRFProtection = True

    @button.buttonAndHandler(_(u"Rebuild membrane catalog"))
    def handleRebuild(self, action):
        catalog = getToolByName(self.context, 'portal_catalog')
        membrane_tool = getToolByName(self.context, 'membrane_tool')
        brains = catalog(portal_type="collective.rcse.member")
        for brain in brains:
            user = brain.getObject()
            membrane_tool.reindexObject(user)


class MaintenanceView(BrowserView):
    def __call__(self):
        self.rebuildMembraneCatalog =\
            RebuildMembraneCatalogForm(self.context, self.request)
        self.rebuildMembraneCatalog.update()
        return self.index()
