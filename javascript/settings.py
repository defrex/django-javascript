
import os
from django.conf import settings

JS_DIR = getattr(settings, 'JS_DIR', os.path.join(settings.STATIC_ROOT, 'js'))
JS_STATIC_ROOT = getattr(settings, 'JS_STATIC_ROOT', settings.STATIC_ROOT)
JS_USE_COMPILED = getattr(settings, 'USE_COMPILED_JS', (not settings.DEBUG))
JS_COMPILED_LOC = getattr(settings, 'COMPILED_JS_LOC', os.path.join(JS_DIR, 'compiled.js'))
JS_COMPILATION_LEVEL = getattr(settings, 'JS_COMPILATION_LEVEL', 'SIMPLE_OPTIMIZATIONS')
JS_INCLUDE_RECURSIVELY = getattr(settings, 'INCLUDE_JS_RECURSIVELY', True)

STATIC_ROOT = settings.STATIC_ROOT
STATIC_URL = settings.STATIC_URL
