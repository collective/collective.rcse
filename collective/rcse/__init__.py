__import__('pkg_resources').declare_namespace(__name__)
import content.event
import permissions
import sys
permissions  # flake8
content.event  # flake 8
try:
    import collective.requestaccess
    collective.requestaccess
except ImportError:
    import requestaccess
    sys.modules['collective.requestaccess'] = requestaccess
