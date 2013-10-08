import datetime
from plone.app.uuid.utils import uuidToObject
from collective.rcse.utils import createNotification
from zope.component.hooks import getSite


def handle_request_added(context, event):
    target = uuidToObject(context.target)
    if context.rtype == 'request':
        where = '/'.join(target.getPhysicalPath())
        what = 'request_access_request'
        when = datetime.datetime.now()
        who = [context.creatorid]
        local_roles = target.get_local_roles()
        for user, role in local_roles:
            if [r for r in role if r in ('Owner', 'Site Administrator')]:
                createNotification(what, where, when, who, user)
    elif context.rtype == 'invitation':
        root = getSite().portal_url.getPortalObject().absolute_url()
        where = '%s/@@my_requests_view' % root
        what = 'request_access_invitation'
        when = datetime.datetime.now()
        who = [context.creatorid]
        user = context.userid
        createNotification(what, where, when, who, user)


def _handle_request(context, event, what):
    target = uuidToObject(context.target)
    if target is None or context.rtype == 'invitation':
        root = getSite().portal_url.getPortalObject().absolute_url()
        where = '%s/@@my_requests_view' % root
    else:
        where = '/'.join(target.getPhysicalPath())
    when = datetime.datetime.now()
    if context.rtype == 'request':
        who = [] # We can't know who validated it
        user = context.userid
    elif context.rtype == 'invitation':
        who = [context.userid]
        user = context.creatorid
    createNotification(what, where, when, who, user)


def handle_request_validated(context, event):
    _handle_request(context, event, 'request_access_validated')


def handle_request_refused(context, event):
    _handle_request(context, event, 'request_access_refused')
