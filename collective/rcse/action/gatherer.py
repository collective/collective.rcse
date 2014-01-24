from AccessControl.unauthorized import Unauthorized
from Acquisition import aq_parent

from collective.whathappened.gatherer_backend import UserActionGathererBackend


class RcseUserActionGathererBackend(UserActionGathererBackend):
    def _getSubscriptionInTree(self, path):
        context = None
        while '/' in path and path != '/':
            subscription = self.storage.getSubscription(path)
            if subscription is not None:
                break
            try:
                if context is None:
                    context = self.context.restrictedTraverse(path)
                else:
                    context = aq_parent(context)
                # Conversation does not have a portal_type attribute !
                if getattr(context, 'portal_type', '') \
                        == 'collective.rcse.group':
                    break
            except KeyError:
                pass
            except Unauthorized:
                pass
            path = path.rpartition('/')[0]
        return subscription
