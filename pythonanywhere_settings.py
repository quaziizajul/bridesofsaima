"""
PythonAnywhere-specific settings overrides
Add this to the end of your settings.py file on PythonAnywhere

Usage in settings.py:
# At the end of settings.py on PythonAnywhere, add:
# from .pythonanywhere_settings import *
"""

import os
import logging
from pathlib import Path

# These will be imported from main settings.py
# BASE_DIR and MEDIA_ROOT should already be defined when this is imported

# Enhanced logging for media file operations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'BridesOfSaima': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Create logs directory if it doesn't exist
log_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(log_dir, exist_ok=True)

# Ensure media directories exist with proper permissions
def ensure_media_directories():
    """Ensure all media directories exist with proper permissions"""
    directories = [
        MEDIA_ROOT,
        os.path.join(MEDIA_ROOT, 'brides'),
        os.path.join(MEDIA_ROOT, 'brides', 'additional'),
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            # Set permissions (755) on Unix systems
            if os.name != 'nt':
                import stat
                os.chmod(directory, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        except Exception as e:
            print(f"Warning: Could not create/set permissions for {directory}: {e}")

# Call the function to ensure directories exist
ensure_media_directories()

# File upload settings for PythonAnywhere
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'tmp')
os.makedirs(FILE_UPLOAD_TEMP_DIR, exist_ok=True)

# Maximum file size (50MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800

# Force Django to use filesystem storage
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'