from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel import model
from zope.i18n import translate
from zope.interface.interface import InterfaceClass
from zope import schema

from collective.rcse.i18n import _

NAMESPACE = 'rcse_visbility_'


class addVisibilityCheckbox(object):
    """This decorator add visbility bool to a SchemaClass
    (plone.supermodel.model.Schema) for every argument not in the blacklist."""

    def __init__(self, privacy_blacklist = []):
        self.privacy_blacklist = privacy_blacklist

    def __call__(self, iface):
        attrs = iface.__dict__['_InterfaceClass__attrs'].items()
        fields = {}
        for name, attr in attrs:
            if name in self.privacy_blacklist:
                continue
            if isinstance(attr, schema.Field):
                field = schema.Bool(
                    title=_(u'Display: ${attr}',
                            mapping={'attr': attr.title})
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
