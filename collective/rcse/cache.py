import hashlib
import os
import threading
import memcache

from plone.memoize import ram
from plone.memoize.volatile import _marker
from plone.memoize.interfaces import ICacheChooser
from zope import component
from zope.interface import directlyProvides


thread_local = threading.local()


def get_client(fun_name):
    global servers

    client = getattr(thread_local, "client", None)
    if client is None:
        servers = os.environ.get(
            "MEMCACHE_SERVER",
            "127.0.0.1:11211"
        ).split(",")
        client = thread_local.client = memcache.Client(servers, debug=0)
    return client


def choose_cache(fun_name):
    client = get_client(fun_name)
    return ram.MemcacheAdapter(client)

directlyProvides(choose_cache, ICacheChooser)


def get_cache(module, fun):
    key = '%s.%s' % (module, fun)
    client = get_client(key)
    return client


def clearCacheKeyGroupAddPermission(username):
    module = 'collective.rcse.content.vocabularies'
    fun = '_getGroupsWithAddPermission'
    key = '%s.%s:%s' % (module, fun, username)
    cache = get_cache(module, fun)
    # We need to set it to None to update the value
    # (Only for memcache! See plone.memoize)
    cache.set(hashlib.md5(key).hexdigest(), None)


def getCacheKeyGroupAddPermission(fun, username):
    return username


def handleUserRolesModifiedOnObject(event):
    clearCacheKeyGroupAddPermission(event.username)
