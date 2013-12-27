from zope import component
from zope import schema
from zope import interface
from zope.formlib import form

from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets.portlets import base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.rcse.i18n import RCSEMessageFactory as _
from collective.rcse.i18n import _p
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from collective.rcse.content.group import get_group


class IPortlet(IPortletDataProvider):
    """A portlet which renders external content using oembed service"""

    header = schema.TextLine(
        title=_p(u"Portlet header"),
        description=_p(u"Title of the rendered portlet"),
        required=False
    )

    count = schema.Int(
        title=_(u"Limit"),
        required=True,
        default=10
    )

    ptype = schema.Choice(
        title=_(u"Portal Type"),
        description=_(u"Choose type to filter."),
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        required=False
    )

    group = schema.Bool(
        title=_(u"Filter on group"),
        description=_(u"Display only content from the current group"),
        default=True)


class Assignment(base.Assignment):
    interface.implements(IPortlet)

    header = _(u"title_portlet", default=u"XItems portlet")
    count = 10
    ptype = None
    group = True

    def __init__(self, header=u"", ptype=None, group=True, count=10):
        self.header = header
        self.ptype = ptype
        self.group = group
        self.count = count

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('xitems.pt')

    def title(self):
        return self.data.title

    def get_items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = self.get_query()
        return catalog(**query)

    def get_query(self):
        query = {"sort_on": "effective", "sort_limit": self.data.count}
        if self.data.ptype:
            query['portal_type'] = self.data.ptype
        group = get_group(self.context)
        if self.data.group and group:
            query['path'] = {'query' : '/'.join(group.getPhysicalPath()),
                             'depth': 1}
        return query


class AddForm(base.AddForm):
    """add form"""
    form_fields = form.Fields(IPortlet)
    label = _(u"title_add_portlet", default=u"Add x items portlet")
    description = _(u"description_portlet",
                    default=u"A portlet which renders x last items")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(IPortlet)
    label = _(u"title_edit_portlet",
              default=u"Edit x items portlet")
    description = _(u"description_portlet",
                    default=u"A portlet which renders x content")
