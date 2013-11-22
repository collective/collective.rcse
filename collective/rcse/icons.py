import logging

logger = logging.getLogger('collective.rcse')


def getStatus(t):
    if t in ['private', 'closed']:
        return 'icon-lock'
    if t in ['internally_published', 'open']:
        return 'icon-unlock'
    if t in ['moderated', 'draft']:
        return 'icon-unlock-alt'
    if t in ['deleted']:
        return 'icon-trash'
    logger.info('No icon for status: %s' % t)
    return ''


def getType(t, prefix=None):
    """Return the icon to use. it use font-awesome syntax: icon-XX
    if you use this is jquerymobile you must add prefix="ui-"
    """
    type2icon = {
        'video': 'icon-film',
        'image': 'icon-picture',
        'file': 'icon-file-alt',
        'event': 'icon-calendar',
        'discussion': 'icon-comments',
        'comment': 'icon-comments',
        'signet': 'icon-bookmark-empty',
        'favori': 'icon-bookmark-empty',
        'link': 'icon-external-link',
        'article': 'icon-edit',
        'poll': 'icon-bar-chart',
        'etherpad': 'icon-cloud',
        'audio': 'icon-volume-up',
        'sound': 'icon-volume-up',
        'folder': 'icon-folder-open',
        'group': 'icon-group',
        'timeline': 'icon-reorder'
    }
    t = t.lower()
    if prefix is None:
        prefix = ""
    for type, icon in type2icon.items():
        if type in t:
            return icon
    logger.info('No icon for type: %s' % t)
    return ""
