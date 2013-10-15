import logging

from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five.browser import BrowserView
from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from collective.rcse.content.proxygroup import ProxyGroupSchema
from zope import interface

logger = logging.getLogger("collective.rcse")


class GroupSchema(form.Schema):
    """Marker interface"""


def get_group(context):
    """
    -> the closest group lookedup in parent of the context
    -> None if context is outside of a group
    """
    if ProxyGroupSchema.providedBy(context):
        return context

    parent = context
    while not GroupSchema.providedBy(parent) and \
            not IPloneSiteRoot.providedBy(parent):
        if parent is None:
            return
        parent = aq_parent(parent)

    if IPloneSiteRoot.providedBy(parent):
        return

    return parent
