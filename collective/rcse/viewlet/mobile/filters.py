import urllib
from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform.layout import FormWrapper
from plone.z3cform import z2
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import form
from z3c.form import button
from z3c.form import widget
from z3c.form.interfaces import IFormLayer
from z3c.form.browser.select import SelectFieldWidget
from zope import component
from zope import schema
from zope import interface

from collective.rcse.i18n import _
from collective.rcse.content.vocabularies import sortBy


class FiltersFormSchema(model.Schema):
    """A set of filters option to select which
    object should be displayed in a group."""

    SearchableText = schema.TextLine(
        title=_(u'Search'),
        required=False
        )

    types = schema.List(
        title=_(u'Types'),
        value_type=schema.Choice(
            vocabulary='collective.rcse.vocabulary.groupTypes'
            ),
        required=False
        )

    sort_on = schema.Choice(
        title=_(u'Sort on'),
        vocabulary=sortBy
        )

    sort_order = schema.Bool(
        title=_(u'Reversed')
        )


class FiltersFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(FiltersFormSchema)

    def __init__(self, context):
        self.context = context
        self.types = []
        self.sort_by = 'date'
        self.reversed = True


class FiltersForm(AutoExtensibleForm, form.Form):
    schema = FiltersFormSchema

    def updateWidgets(self):
        self.fields['types'].widgetFactory = SelectFieldWidget
        super(FiltersForm, self).updateWidgets()
        self.widgets['types'].multiple = 'multiple'
        if self.request.get('SearchableText'):
            self.widgets['SearchableText'].value =\
                self.request.get('SearchableText')
        if self.request.get('types'):
            self.widgets['types'].value = self.request.get('types')
        if self.request.get('sort_on'):
            self.widgets['sort_on'].value = self.request.get('sort_on')
        if self.request.get('sort_order') == 'reverse':
            self.widgets['sort_order'].items[0]['checked'] = True

    @button.buttonAndHandler(_(u'Filter'))
    def filter(self, action):
        data, errors = self.extractData()
        if data['types'] is not None:
            data['types'] = ','.join(data['types'])
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
        self.form = FiltersForm(aq_inner(self.context), self.request)
        interface.alsoProvides(self.form, IWrappedForm)
        self.form.update()
