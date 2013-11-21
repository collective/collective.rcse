import unittest2 as unittest
from collective.requestaccess.tests import base
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes


class TestSetup(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def test_browserlayer(self):
        from plone.browserlayer import utils
        from collective.requestaccess import layer
        self.assertIn(layer.Layer, utils.registered_layers())

    def test_types(self):
        types = self.layer['portal'].portal_types
        _type = 'collective.requestaccess'
        actions = types.listActions(object=_type)
        self.assertIsNotNone(actions)

    def test_upgrades(self):
        profile = 'collective.requestaccess:default'
        setup = self.layer['portal'].portal_setup
        upgrades = setup.listUpgrades(profile, show_old=True)
        self.assertTrue(len(upgrades) > 0)
        for upgrade in upgrades:
            upgrade['step'].doStep(setup)

    def test_setuphandler(self):
        self.assertIn('portal_requestaccess', self.layer['portal'].objectIds())
        container = self.layer['portal'].portal_requestaccess
        self.assertEqual(container.getLayout(),
                         'folder_full_view')
        aspect = ISelectableConstrainTypes(container)
        addable = aspect.getImmediatelyAddableTypes()
        type_name = "collective.requestaccess"
        self.assertIn(type_name, addable)

    def test_type_not_searched(self):
        properties = self.layer['portal'].portal_properties.site_properties
        tns = properties.getProperty('types_not_searched')
        type_name = "collective.requestaccess"
        self.assertIn(type_name, tns)
        self.assertNotEqual(len(tns), 1)  # not purged


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
