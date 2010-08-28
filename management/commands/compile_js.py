
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from javascript.js import GoogleClosureMinifier, JavaScriptCompiler, DummyMinifier
from javascript.models import JSVersion

class Command(BaseCommand):
    help = 'Compile Javascript'

    def handle(self, *args, **options):
        print 'Begining JS Compilation...'
        
        cur_dir = os.path.dirname(__file__)
        closure_jar = os.path.join(cur_dir, '../../closure-compiler.jar')
        minifier = GoogleClosureMinifier(closure_jar)
        #minifier = DummyMinifier()
        
        jsc = JavaScriptCompiler(settings.JS_DIR, minifier,
                compiled_loc=settings.COMPILED_JS_LOC, v=True,
                recurse=settings.INCLUDE_JS_RECURSIVELY)
        jsc.compile_js()
        
        js_version, c = JSVersion.objects.get_or_create(pk=1)
        js_version.version += 1
        js_version.save()
        
        print 'JS at version %s.' % str(js_version.version)
        