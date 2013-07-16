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
from z3c.form.interfaces import IFormLayer
from zope import component
from zope import schema
from zope import interface

from collective.rcse.i18n import _
from collective.rcse.content.vocabularies import sortBy


class FiltersFormSchema(model.Schema):
    """A set of filters option to select which
    object should be displayed in a group."""

    types = schema.List(
        title=_(u'Types'),
        value_type=schema.Choice(
            vocabulary='collective.rcse.vocabulary.groupTypes'
            )
        )

    sort_by = schema.Choice(
        title=_(u'Sort by'),
        vocabulary=sortBy
        )

    reversed = schema.Bool(
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

    @button.buttonAndHandler(_(u'Filter'))
    def filter(self, action):
        data, errors = self.extractData()
        import pdb; pdb.set_trace()


class FiltersFormView(ViewletBase):
    def update(self):
        super(FiltersFormView, self).update()
        z2.switch_on(self, request_layer=IFormLayer)
        self.form = FiltersForm(aq_inner(self.context), self.request)
        interface.alsoProvides(self.form, IWrappedForm)
        self.form.update()
