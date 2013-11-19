from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter

from collective.polls import MessageFactory as _


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

        if 'poll.submit' in form:
            self._handleSubmit(form)
        # Update status messages
        for error in self.errors:
            messages.addStatusMessage(error, type="warn")
        for msg in self.messages:
            messages.addStatusMessage(msg, type="info")

    def _handleSubmit(self, form):
        INVALID_OPTION = _(u'Invalid option')
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
