from Products.CMFPlone.utils import getToolByName
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest

from collective.rcse.content.utils import createCompany


def createCompanyIfNotExists(context, event):
    if event.new_state.id != 'enabled':
        return
    request = getRequest()
    portal_state = getMultiAdapter((context, request),
                                   name=u'plone_portal_state')
    directory = portal_state.portal()['companies_directory']
    if not context.company_id or context.company_id not in directory:
        mtool = getToolByName(context, 'portal_membership')
        context.company_id = createCompany(context, request)
