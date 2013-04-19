#python
import sys, logging

#zope
import transaction
from zope.component import getSiteManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Testing.makerequest import makerequest
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy
from Products.CMFCore.tests.base.security import OmnipotentUser
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import setSite

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
lformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(lformat)
handler.setFormatter(formatter)
logger.addHandler(handler)
POLICY = 'collective.rcse'
PROFILE = 'profile-%s:default' % POLICY


def quickinstall_addons(context, install=None, uninstall=None, upgrades=None):
    logger = logging.getLogger(PROFILE)
    qi = getToolByName(context, 'portal_quickinstaller')

    if install is not None:
        for addon in install:
            if qi.isProductInstallable(addon):
                qi.installProduct(addon)
            else:
                logger.error('%s can t be installed' % addon)

    if uninstall is not None:
        qi.uninstallProducts(uninstall)

    if upgrades is not None:
        if upgrades in ("all", True):
            #TODO: find which addons should be upgrades
            installedProducts = qi.listInstalledProducts(showHidden=True)
            upgrades = [p['id'] for p in installedProducts]
        for upgrade in upgrades:
            # do not try to upgrade myself -> recursion
            if upgrade == POLICY:
                continue
            try:
                qi.upgradeProduct(upgrade)
            except KeyError:
                logger.error('can t upgrade %s' % upgrade)


def common(context):

    portal_migration = getToolByName(context, 'portal_migration')
    portal_migration.upgrade()
    logger.info("Ran Plone Upgrade")

    #upgrades installed addons
    quickinstall_addons(context, upgrades=True)

    context.runAllImportStepsFromProfile(PROFILE)
    logger.info("Applied %s" % PROFILE)


if "app" in locals():
    # Use Zope application server user database (not plone site)
    # spoof request
    _policy = PermissiveSecurityPolicy()
    _oldpolicy = setSecurityPolicy(_policy)
    admin = app.acl_users.getUserById("admin")
    newSecurityManager(None, admin)
    app = makerequest(app)

    plone = app.restrictedTraverse("Plone")
    setSite(plone)
    plone.setupCurrentSkin(app.REQUEST)

    common(plone.portal_setup)

    transaction.commit()
    # Perform ZEO client synchronization (if runnning in clustered mode)
    app._p_jar.sync()
