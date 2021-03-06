import urllib
from plone.app.z3cform import layout
from plone.autoform.form import AutoExtensibleForm
from plone.autoform import directives
from plone.supermodel import model
from Products.Five.browser import BrowserView
from z3c.form import form
from z3c.form import button
from z3c.form.browser.select import SelectFieldWidget
from zope import component
from zope import schema
from zope import interface

from collective.rcse.content.group import get_group
from collective.rcse.content.vocabularies import sortBy
from collective.rcse.i18n import _
from collective.rcse.icons import getType


class FiltersFormSchema(model.Schema):
    """A set of filters option to select which
    object should be displayed in a group."""

    SearchableText = schema.TextLine(
        title=_(u'Search'),
        required=False
    )

    directives.widget('portal_type', SelectFieldWidget)
    portal_type = schema.Choice(
        title=_(u'Type'),
        required=False,
        vocabulary='collective.rcse.vocabulary.addableTypes'
    )

    sort_on = schema.Choice(
        title=_(u'Sort on'),
        vocabulary=sortBy,
        default="relevance"
    )

    sort_order = schema.Bool(
        title=_(u'Reversed')
    )


class FiltersFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(FiltersFormSchema)

    def __init__(self, context):
        self.context = context
        self.portal_type = None
        self.sort_on = 'relevance'
        self.reversed = True


class FiltersForm(AutoExtensibleForm, form.Form):
    schema = FiltersFormSchema
    form_name = 'filter_content'

    enableUnloadProtection = False

    def updateWidgets(self):
        super(FiltersForm, self).updateWidgets()
        if self.request.get('SearchableText'):
            self.widgets['SearchableText'].value =\
                self.request.get('SearchableText')
        if self.request.get('portal_type'):
            self.widgets['portal_type'].value = self.request.get('portal_type')
        if self.request.get('sort_on'):
            self.widgets['sort_on'].value = self.request.get('sort_on')
        if self.request.get('sort_order') == 'reverse':
            self.widgets['sort_order'].items[0]['checked'] = True

    @button.buttonAndHandler(_(u'Filter'))
    def filter(self, action):
        data, errors = self.extractData()
        if data['sort_order']:
            data['sort_order'] = 'reverse'
        else:
            data['sort_order'] = 'ascending'
        if data['portal_type'] is None:
            del data['portal_type']
        if data['SearchableText'] is None:
            del data['SearchableText']
        params = urllib.urlencode(data)
        self.request.response.redirect('?%s' % params)


class FilterButton(layout.FormWrapper):
    """button"""
    form = FiltersForm


class FilterButtonView(BrowserView):
    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
            )

    def group_url(self):
        group = get_group(self.context)
        if group is None:
            group_url = self.portal_state.navigation_root_url()
            if not group_url.endswith('/home'):
                group_url += '/home'
        else:
            group_url = group.absolute_url()
        return group_url

    def get_icon(self, term):
        return getType(term)
