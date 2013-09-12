

def get(t, prefix=None):
    """Return the icon to use. it use font-awesome syntax: icon-XX
    if you use this is jquerymobile you must add prefix="ui-"
    """
    t = t.lower()
    if 'video' in t:
        return 'icon-film'
    elif 'image' in t:
        return 'icon-picture'
    elif 'file' in t:
        return 'icon-file-alt'
    elif 'event' in t:
        return 'icon-calendar'
    elif 'discussion' in t or 'comment' in t:
        return 'icon-comments'
    elif 'signet' in t or 'favori' in t:
        return 'icon-bookmark-empty'
    elif 'link' in t:
        return 'icon-external-link'
    elif 'blog' in t or 'document' in t or 'news' in t:
        return 'icon-edit'
    elif 'poll' in t:
        return 'icon-bar-chart'
    elif 'etherpad' in t:
        return 'icon-cloud'
    elif 'audio' in t or 'sound' in t:
        return 'icon-volume-up'
    elif 'folder' in t:
        return 'icon-folder-open'
    elif 'group' in t:
        return 'icon-group'
#    elif '' in t:
#        return 'icon-'
    return ""
