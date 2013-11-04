import urllib
from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from plone.autoform.form import AutoExtensibleForm
from plone.autoform import directives
from plone.supermodel import model
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform import z2
from z3c.form import form
from z3c.form import button
from z3c.form.interfaces import IFormLayer
from z3c.form.browser.select import SelectFieldWidget
from zope import component
from zope import schema
from zope import interface

from collective.rcse.i18n import _
from collective.rcse.content.vocabularies import sortBy
from collective.rcse.page.controller.addbutton import AddForm


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
        if data['SearchableText'] is None:
            del data['SearchableText']
        params = urllib.urlencode(data)
        self.request.response.redirect('?%s' % params)


class FiltersFormView(ViewletBase):
    def update(self):
        super(FiltersFormView, self).update()
        z2.switch_on(self, request_layer=IFormLayer)
        context = aq_inner(self.context)
        self.form_filter = FiltersForm(context, self.request)
        interface.alsoProvides(self.form_filter, IWrappedForm)
        self.form_filter.update()

        self.form_addbutton = AddForm(context, self.request)
        interface.alsoProvides(self.form_addbutton, IWrappedForm)
        self.form_addbutton.update()
