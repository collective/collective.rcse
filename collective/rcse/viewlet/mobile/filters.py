from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform import z2
from z3c.form.interfaces import IFormLayer
from zope import interface

from collective.rcse.page.controller.addbutton import AddForm
from collective.rcse.page.controller.filterbutton import FiltersForm


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
