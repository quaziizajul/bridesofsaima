# PythonAnywhere WSGI Configuration
import os
import sys

# Add your project directory to Python path
path = '/home/yourusername/BridesOfSaimaPortal'
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'BridesOfSaimaPortal.production_settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()