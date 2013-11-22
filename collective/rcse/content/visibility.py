from collections import OrderedDict
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel import model
from zope import schema
from zope.schema._schema import getFieldsInOrder

from collective.rcse.i18n import _

NAMESPACE = 'rcse_visbility_'


class addVisibilityCheckbox(object):
    """This decorator add visbility bool to a SchemaClass
    (plone.supermodel.model.Schema) for every argument not in the blacklist."""

    def __init__(self, privacy_blacklist=[]):
        self.privacy_blacklist = privacy_blacklist

    def __call__(self, iface):
        #attrs = iface.__dict__['_InterfaceClass__attrs'].items()
        attrs = getFieldsInOrder(iface)
        fields = OrderedDict()
        for name, attr in attrs:
            if name in self.privacy_blacklist:
                continue
            if isinstance(attr, schema.Field):
                field = schema.Bool(
                    title=_(u'Hide: ${attr}',
                            mapping={'attr': attr.title}),
                    required=False
                )
                fields['%s%s' % (NAMESPACE, name)] = field
        fieldset = model.Fieldset(
            'privacy',
            label=_(u'Privacy'),
            fields=[f for f in fields.keys()]
        )
        new_iface = model.SchemaClass(iface.__name__, (iface,), fields)
        new_iface.setTaggedValue(FIELDSETS_KEY, [fieldset])
        return new_iface
