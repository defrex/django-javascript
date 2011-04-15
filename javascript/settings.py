
import os
from django.conf import settings

JS_DIR = getattr(settings, 'JS_DIR', os.path.join(settings.MEDIA_ROOT, 'js'))
USE_COMPILED_JS = getattr(settings, 'USE_COMPILED_JS', (not settings.DEBUG))
COMPILED_JS_LOC = getattr(settings, 'COMPILED_JS_LOC', JS_DIR)
#COMPILED_JS_LOC = getattr(settings, 'COMPILED_JS_LOC', os.path.join(JS_DIR, 'compiled.js'))
JS_COMPILATION_LEVEL = getattr(settings, 'JS_COMPILATION_LEVEL', 'SIMPLE_OPTIMIZATIONS')
INCLUDE_JS_RECURSIVELY = getattr(settings, 'INCLUDE_JS_RECURSIVELY', True)

MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
