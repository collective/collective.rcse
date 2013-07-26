from Acquisition import aq_parent
from plone.directives import form
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot


class GroupSchema(form.Schema):
    """Marker interface"""


def get_group(context):
    """
    -> the closest group lookedup in parent of the context
    -> None if context is outside of a group
    """
    parent = context

    while not GroupSchema.providedBy(parent) and \
            not IPloneSiteRoot.providedBy(parent):
        parent = aq_parent(parent)

    if IPloneSiteRoot.providedBy(parent):
        return

    return parent
