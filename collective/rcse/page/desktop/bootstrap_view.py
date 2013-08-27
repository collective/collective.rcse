from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface
from Products.Five import BrowserView
from plone.app.layout.navigation.navtree import buildFolderTree
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder


class IBootstrapView(Interface):
    def getColumnsClasses(view=None):
        """Return the viewport
        """

class BootstrapView(BrowserView):

    def getColumnsClasses(self, view=None):
        """ Determine whether a column should be shown. The left column is
            called plone.leftcolumn; the right column is called
            plone.rightcolumn.
        """

        plone_view = getMultiAdapter(
            (self.context, self.request), name=u'plone')
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')

        sl = plone_view.have_portlets('plone.leftcolumn', view=view)
        sr = plone_view.have_portlets('plone.rightcolumn', view=view)

        isRTL = portal_state.is_rtl()

        # pre-fill dictionary
        columns = dict(one="", content="", two="")

        #http://getbootstrap.com/css/#grid-options

        if not sl and not sr:
            # we don't have columns, thus conten takes the whole width
            columns['content'] = "col-md-12 col-lg-12"

        elif sl and sr:
            # In case we have both columns, content takes 50% of the whole
            # width and the rest 50% is spread between the columns
            columns['one'] = "col-md-3 col-lg-3"
            columns['content'] = "col-md-6 col-lg-5"
            columns['two'] = "col-md-3 col-lg-4"

        elif sr and not sl:
            # We have right column and we are NOT in RTL language
            columns['content'] = "col-md-9 col-lg-8"
            columns['two'] = "col-md-3 col-lg-4"

        elif sl and not sr:
            # We have left column and we are in NOT RTL language
            columns['one'] = "col-md-3 col-lg-3"
            columns['content'] = "col-md-8 col-lg-9"

        # # append cell to each css-string
        # for key, value in columns.items():
        #     columns[key] = "cell " + value

        return columns
