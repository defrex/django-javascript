
import os

from django.core.management.base import BaseCommand

from javascript.js import GoogleClosureMinifier, JavaScriptCompiler
from javascript.models import JSVersion
from javascript import settings

class Command(BaseCommand):
    help = 'Compile Javascript'

    def handle(self, *args, **options):
        print 'Begining JS Compilation...'

        cur_dir = os.path.dirname(__file__)
        closure_jar = os.path.join(cur_dir, '../../closure-compiler.jar')
        minifier = GoogleClosureMinifier(closure_jar)
        #minifier = DummyMinifier()

        jsc = JavaScriptCompiler(settings.JS_DIR, minifier,
                compiled_loc=settings.JS_COMPILED_LOC, v=True,
                recurse=settings.JS_INCLUDE_RECURSIVELY)
        jsc.compile_js()

        js_version, c = JSVersion.objects.get_or_create(pk=1)
        js_version.version += 1
        js_version.save()

        print 'JS at version %s.' % str(js_version.version)
