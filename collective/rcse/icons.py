import logging


logger = logging.getLogger('collective.rcse')

def getStatus(t):
    if t in ['private', 'closed']:
        return 'icon-lock'
    if t in ['internally_published', 'open']:
        return 'icon-unlock'
    if t in ['moderated']:
        return 'icon-unlock-alt'
    logger.info('No icon for status: %s' % t)
    return ''

def getType(t, prefix=None):
    """Return the icon to use. it use font-awesome syntax: icon-XX
    if you use this is jquerymobile you must add prefix="ui-"
    """
    t = t.lower()
    if prefix is None:
        prefix = ""
    if 'video' in t:
        return prefix + 'icon-film'
    elif 'image' in t:
        return prefix + 'icon-picture'
    elif 'file' in t:
        return prefix + 'icon-file-alt'
    elif 'event' in t:
        return prefix + 'icon-calendar'
    elif 'discussion' in t or 'comment' in t:
        return prefix + 'icon-comments'
    elif 'signet' in t or 'favori' in t:
        return prefix + 'icon-bookmark-empty'
    elif 'link' in t:
        return prefix + 'icon-external-link'
    elif 'blog' in t or 'document' in t or 'news' in t:
        return prefix + 'icon-edit'
    elif 'poll' in t:
        return prefix + 'icon-bar-chart'
    elif 'etherpad' in t:
        return prefix + 'icon-cloud'
    elif 'audio' in t or 'sound' in t:
        return prefix + 'icon-volume-up'
    elif 'folder' in t:
        return prefix + 'icon-folder-open'
    elif 'group' in t:
        return prefix + 'icon-group'
    elif 'timeline' in t:
        return prefix + 'icon-reorder'
#    elif '' in t:
#        return 'icon-'
    logger.info('No icon for type: %s' % t)
    return ""
