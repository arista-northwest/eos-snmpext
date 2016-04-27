
import importlib
import os
import re
import sys
def _load_module(name):
    """Load protocol module from name"""

    package = None
    if __name__ == '__main__':
        package = 'eos_snmpext'
    else:
        package, _ = __name__.split('.', 1)

    path = '.'.join((package, 'extensions', name))
    module = importlib.import_module(path)

    return getattr(module, 'update')


#print [m for m in os.listdir(sys.argv[1]) if m.endswith('.py') and not m.startswith('_')]

def get_modules(path):
    modules = []
    for item in os.listdir(path):
        if re.match('^[a-z0-9].*\.py$', item, re.I):
            print item


#from snmp_extensions.util import

# extensions = {k: v for k, v in sys.modules.iteritems() if 'eos_snmpext.extensions.' in k}
# print extensions.keys()
# exit()

# def _load_extensions():
#     for path in PATHS:
#
#         path = os.path.abspath(os.path.expanduser(path))
#
#         if not os.path.exists(path):
#             continue
#
#         if path not in sys.path:
#             sys.path.insert(1, path)
#
#         modules = []
#         for item in os.listdir(path):
#             if re.match('^[a-z0-9].*\.py$', item, re.I):
#                 print item

get_modules(sys.argv[1])
