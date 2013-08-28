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
            "plonetheme.jquerymobile",
        ]
        for name in dependencies:
            self.assertTrue(qi.isProductInstalled(name))

    def test_type_group(self):
        ptypes = self.portal.portal_types
        gtype = ptypes.getTypeInfo("collective.rcse.group")
        self.assertEqual(gtype.Title(), u"Group")
        self.login("Manager")
        self.assertTrue(gtype.isConstructionAllowed(self.portal))
        self.login("Member")
        self.assertFalse(gtype.isConstructionAllowed(self.portal))
        self.assertTrue(gtype.allowDiscussion())
        self.assertTrue(gtype.globalAllow())
        self.assertEqual(gtype.add_permission, "collective.rcse.AddGroup")

    def test_group_contents(self):
        ptypes = self.portal.portal_types
        gtype = ptypes.getTypeInfo("collective.rcse.group")
        for content in (
            "audio",
            "document",
            "event",
            "file",
            "image",
            "video",
        ):
            ctype = "collective.rcse." + content
            self.assertTrue(gtype.allowType(ctype))
            info = ptypes.getTypeInfo(ctype)
            self.assertTrue(info.allowDiscussion())
            self.assertFalse(info.globalAllow())
            addperm = "collective.rcse.Add" + content.capitalize()
            self.assertEqual(info.add_permission, addperm)

    def test_type_audio(self):
        ptypes = self.portal.portal_types
        gtype = ptypes.getTypeInfo("collective.rcse.audio")
        self.assertEqual(gtype.Title(), u"Audio")

    def test_type_event(self):
        ptypes = self.portal.portal_types
        gtype = ptypes.getTypeInfo("collective.rcse.event")
        self.assertEqual(gtype.Title(), u"Event")

    def test_type_file(self):
        ptypes = self.portal.portal_types
        gtype = ptypes.getTypeInfo("collective.rcse.file")
        self.assertEqual(gtype.Title(), u"File")

    def test_type_image(self):
        ptypes = self.portal.portal_types
        gtype = ptypes.getTypeInfo("collective.rcse.image")
        self.assertEqual(gtype.Title(), u"Image")

    def test_type_video(self):
        ptypes = self.portal.portal_types
        gtype = ptypes.getTypeInfo("collective.rcse.video")
        self.assertEqual(gtype.Title(), u"Video")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
