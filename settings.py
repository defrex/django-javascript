
import os
from django.conf import settings

USE_COMPILED_JS = getattr(settings, 'USE_COMPILED_JS', (not settings.DEBUG))
COMPILED_JS_LOC = getattr(settings, 'COMPILED_JS_LOC', 'compiled.js')
JS_COMPILATION_LEVEL = getattr(settings, 'JS_COMPILATION_LEVEL', 'SIMPLE_OPTIMIZATIONS')
INCLUDE_JS_RECURSIVELY = getattr(settings, 'INCLUDE_JS_RECURSIVELY', True)
JS_DIR = getattr(settings, 'JS_DIR', os.path.join(settings.MEDIA_ROOT, 'js'))

MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
