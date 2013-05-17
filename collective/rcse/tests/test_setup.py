import unittest2 as unittest
from collective.rcse.tests import base


class TestSetup(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """
    def test_dependencies_installed(self):
        qi = self.portal.portal_quickinstaller
        dependencies = [
            "cioppino.twothumbs",
            "collective.etherpad",
            "collective.history",
            "collective.js.ckeditor",
            "collective.mediaelementjs",
            "collective.picturefill",
            "collective.themeswitcher",
            "plone.app.dexterity",
            "plonetheme.foundation",
            "plonetheme.jquerymobile",
        ]
        for name in dependencies:
            self.assertTrue(qi.isProductInstalled(name))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
