import unittest

#import robotsuite
#from collective.rcse.testing import ROBOT
#from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
#    suite.addTests([
#        layered(robotsuite.RobotTestSuite('test_robot.robot'),
#                layer=ROBOT),
#    ])
    return suite
