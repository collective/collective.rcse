from AccessControl import Unauthorized
from Acquisition import aq_inner, aq_parent
 
from zope import schema
 
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import queryUtility
 
from zope.interface import invariant, Invalid
 
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
 
from plone.directives import dexterity
from plone.directives import form
 
from collective.z3cform.widgets.enhancedtextlines import EnhancedTextLinesFieldWidget
 
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.interfaces import ISiteRoot
 
from collective.polls.config import COOKIE_KEY
from collective.polls.config import MEMBERS_ANNO_KEY
from collective.polls.config import VOTE_ANNO_KEY
 
from collective.polls.config import PERMISSION_VOTE
 
from collective.polls.polls import IPolls
 
from collective.polls import MessageFactory as _
from Products.Five.browser import BrowserView
 
 
class PollView(BrowserView):
 
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
#        super(PollView, self).update()
        messages = IStatusMessage(self.request)
        context = aq_inner(self.context)
        self.context = context
        self.state = getMultiAdapter(
            (context, self.request), name=u'plone_context_state')
        self.wf_state = self.state.workflow_state()
        self.utility = context.utility
        # Handle vote
        form = self.request.form
        self.errors = []
        self.messages = []
 
        #if the poll is open and anonymous should vote but the parent folder
        #is private.. inform the user.
 
        # When the poll's container is the site's root, we do not need to
        # check the permissions.
        container = aq_parent(aq_inner(self.context))
 
#         if 'open' == self.wf_state and not ISiteRoot.providedBy(container):
#             roles = [
#                 r['name'] for r in
#                 self.context.rolesOfPermission('collective.polls: Vote')
#                 if r['selected']]
#  
#             if 'Anonymous' not in roles and self.context.allow_anonymous:
#                 messages.addStatusMessage(_(
#                     u"Anonymous user won't be able to vote, you forgot to "
#                     u"publish the parent folder, you must sent back the poll "
#                     u"to private state, publish the parent folder and open "
#                    u"the poll again"), type="info")
 
        INVALID_OPTION = _(u'Invalid option')
        if 'poll.submit' in form:
            options = form.get('options', '')
            if isinstance(options, list):
                self.errors.append(INVALID_OPTION)
            elif isinstance(options, str):
                if not options.isdigit():
                    self.errors.append(INVALID_OPTION)
                else:
                    options = int(options)
            if not self.errors:
                # Let's vote
                try:
                    self.context.setVote(options, self.request)
                    self.messages.append(_(u'Thanks for your vote'))
                    # We do this to avoid redirecting anonymous user as
                    # we just sent them the cookie
                    self._has_voted = True
                except Unauthorized:
                    self.errors.append(_(u'You are not authorized to vote'))
        # Update status messages
        for error in self.errors:
            messages.addStatusMessage(error, type="warn")
        for msg in self.messages:
            messages.addStatusMessage(msg, type="info")
 
        # XXX
        #if 'voting.from' in form:
            #url = form['voting.from']
            #self.request.RESPONSE.redirect(url)
 
    @property
    def can_vote(self):
        if hasattr(self, '_has_voted') and self._has_voted:
            # This is mainly to avoid anonymous users seeing the form again
            return False
        try:
            return self.utility.allowed_to_vote(self.context, self.request)
        except Unauthorized:
            return False
 
    @property
    def can_edit(self):
        utility = self.utility
        return utility.allowed_to_edit(self.context)
 
    @property
    def has_voted(self):
        ''' has the current user voted in this poll? '''
        if hasattr(self, '_has_voted') and self._has_voted:
            return True
        utility = self.utility
        voted = utility.voted_in_a_poll(self.context, self.request)
        return voted
 
    def poll_uid(self):
        ''' Return uid for current poll '''
        utility = self.utility
        return utility.uid_for_poll(self.context)
 
    def getOptions(self):
        ''' Returns available options '''
        return self.context.getOptions()
 
    def getResults(self):
        ''' Returns results so far if allowed'''
        show_results = False
        if self.wf_state == 'open':
            show_results = show_results or self.context.show_results
        elif self.wf_state == 'closed':
            show_results = True
        return (show_results and self.context.getResults()) or None
