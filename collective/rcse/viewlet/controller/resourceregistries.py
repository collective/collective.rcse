import os
import Globals
import json

from copy import copy
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import view
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.publisher.interfaces.browser import IBrowserPublisher

from collective.rcse.i18n import _
from zope.i18n import translate


class ResourcesViewlet(ViewletBase):
    """Display resources for RCSE"""
    index = ViewPageTemplateFile("resourceregistries.pt")
    def __init__(self, context, request, view, manager=None):
        super(ResourcesViewlet, self).__init__(context, request, view, manager=None)
        self.styles_config = []
        self.scripts_config = []

    def update(self):
        super(ResourcesViewlet, self).update()
        self.locales = {
            "readmore_more": self._translate(_(u"Read more")),
            "readmore_close": self._translate(_(u"Close")),
        }
        self.json_locales = json.dumps(self.locales)

    def _translate(self, msg):
        return translate(msg, context=self.request)

    @view.memoize_contextless
    def styles(self):
        return self.add_src_from_id(self.styles_config)

    @view.memoize_contextless
    def scripts(self):
        return self.add_src_from_id(self.scripts_config)

    def add_src_from_id(self, items):
        results = []
        develmode = self.getDevelMode()
        portal = self.portal_state.portal()
        for info in items:
            item = copy(info)
            itemid = item["id"]
            if itemid.startswith('http'):
                info['src'] = itemid
                results.append(info)
            else:
                if '.min.' in itemid and develmode:
                    try:
                        id = itemid.replace(".min.", ".")
                        content = portal.restrictedTraverse(id)
                        itemid = id
                    except KeyError:
                        content = portal.restrictedTraverse(itemid)
                else:
                    content = portal.restrictedTraverse(itemid)
                if content and IBrowserPublisher.providedBy(content):
                    path = content.context.path
                    time = str(os.path.getmtime(path))
                    info["src"] = "%s/%s?time%s" % (self.site_url,
                                                    itemid,
                                                    time)
                    results.append(info)
                elif content:
                    info["src"] = "%s/%s" % (self.site_url,info["id"])
                    results.append(info)
        return results

    def getDevelMode(self):
        """Are we running in development mode?"""
        return bool(Globals.DevelopmentMode)


class DesktopResourceRegistries(ResourcesViewlet):
    def update(self):
        super(DesktopResourceRegistries, self).update()
        self.styles_config.append({
                'rendering': 'link',
                'media': 'screen',
                'rel': 'stylesheet',
                'title': '',
                'conditionalcomment' : "",
                'id': "++resource++collective.rcse/css/desktop.min.css"
        })
        self.scripts_config.append({
            'inline': False,
            'conditionalcomment' : "",
            'id': "plone_javascript_variables.js"
         })
        self.scripts_config.append({
            'inline': False,
            'conditionalcomment' : "",
            'id': "++resource++collective.rcse/js/desktop.min.js"
         })


class MobileResourceRegistries(ResourcesViewlet):
    def update(self):
        super(MobileResourceRegistries, self).update()
        self.styles_config.append({
                'rendering': 'link',
                'media': 'screen',
                'rel': 'stylesheet',
                'title': '',
                'conditionalcomment' : "",
                'id': "++resource++collective.rcse/css/mobile.min.css"
        })
        self.scripts_config.append({
            'inline': False,
            'conditionalcomment' : "",
            'id': "plone_javascript_variables.js"
         })
        self.scripts_config.append({
            'inline': False,
            'conditionalcomment' : "",
            'id': "++resource++collective.rcse/js/mobile.min.js"
         })
