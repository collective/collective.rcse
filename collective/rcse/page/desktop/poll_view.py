from collective.polls.content.poll import View
from five import grok
from collective.rcse import layer

grok.templatedir("templates")


class PollView(View):
    grok.layer(layer.DesktopLayer)
    grok.template("poll_view")
