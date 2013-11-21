__import__('pkg_resources').declare_namespace(__name__)
import permissions
permissions  # flake8
import content.event
content.event  # flake 8

try:
    import collective.request.access
except ImportError:
    import collective.rcse.requestaccess as requestaccess
    sys.modules['collective.requestaccess'] = requestaccess
