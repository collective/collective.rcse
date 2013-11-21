from zope import interface
from zope import schema
from plone.directives import form
from collective.requestaccess.i18n import _


class RequestSchema(form.Schema):
    """Request your access to a group"""
    id = schema.ASCIILine(title=_(u"ID"))
    rtype = schema.Choice(
        title=_(u"Type of request"),
        vocabulary="collective.requestaccess.vocabulary.rtypes"
    )
    creatorid = schema.ASCIILine(title=_(u"Creator ID"))
    userid = schema.ASCIILine(title=_(u"User ID"))
    target = schema.ASCIILine(title=_(u"Target UUID"))
    target_path = schema.List(
        title=_(u"Target Path"),
        value_type=schema.ASCIILine(title=_(u"Target path part")),
    )
    target_title = schema.ASCIILine(title=_(u"Target title"))
    role = schema.Choice(
        title=_(u"Role"),
        vocabulary="collective.requestaccess.vocabulary.roles"
    )


class IRequestManager(interface.Interface):

    def create():
        """Return a proxy request object
        You have next to set the requested role to the role attribute.
        """

    def add(request):
        """Validate and add the request access"""

    def remove(requestid):
        """Remove the corresponding request"""

    def get(query=None):
        """Return a list of request corresponding to the query"""

    def get_current_id():
        """Return the ID of the current request even if it doesn't exists"""

    def get_current():
        """Return the current request. Return None if no request"""

    def can_request():
        """Verify the current authenticated member can request
        for an access on the current context"""

    def can_invite():
        """Verify the current authenticated member can invite a member
        for an access on the current context"""

    def can_review():
        """Verify the current authenticated member can review request access
        """

    def cancel_request():
        """Cancel the current request if exists"""

    def validate(requestid):
        """Validate the request"""

    def refuse(requestid):
        """Refuse the request"""


class Settings(interface.Interface):
    """addon settings"""
    roles = schema.List(
        title=_(u"Roles"),
        value_type=schema.Choice(
            title=_(u"Role"),
            vocabulary="plone.app.vocabularies.Roles"
        ),
    )
