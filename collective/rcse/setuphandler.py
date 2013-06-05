## setuphandlers.py
import logging

LOG = logging.getLogger("collective.history")


def setupVarious(context):
    """Create the history container"""

    if context.readDataFile('collective_rcse.txt') is None:
        return

    portal = context.getSite()
    updateWelcomePage(portal)


def updateWelcomePage(site):
    layout = site.getLayout()
    if layout != "welcome_view":
        site.setLayout("welcome_view")
        LOG.info("set welcome_view as default page")
