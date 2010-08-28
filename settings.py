
import os

from django.conf.settings import *

USE_COMPILED_JS = not DEBUG
JS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                      '../../site_media/js/')
COMPILED_JS_LOC = os.path.join(JS_DIR, 'compiled.js')
JS_COMPILATION_LEVEL = 'SIMPLE_OPTIMIZATIONS'
INCLUDE_JS_RECURSIVELY = True

