from zope import i18nmessageid

RCSEMessageFactory = i18nmessageid.MessageFactory("collective.rcse")
_ = RCSEMessageFactory
_t = i18nmessageid.MessageFactory("collective.rcse.tmp")
_p = i18nmessageid.MessageFactory("plone")

msg_watchers_add = _(
    u"You have added the content of this group to your news"
)
msg_watchers_rm = _(
    u"You have removed the content of this group from your news"
)
_(u"Search groups")
