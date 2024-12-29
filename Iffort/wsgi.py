# wsgi.py
import os
import sys
from django.core.wsgi import get_wsgi_application

print("Current working directory:", os.getcwd())
print("PYTHONPATH:", sys.path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Iffort.settings')

application = get_wsgi_application()
