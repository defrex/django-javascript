from uuid import uuid4
from os.path import join

from django import template
from django.conf import settings

from javascript.js import JavaScriptCompiler
from javascript.models import JSVersion

register = template.Library()

@register.simple_tag
def include_js():
    if settings.USE_COMPILED_JS:
        jsc = JavaScriptCompiler(settings.JS_DIR, 
                compiled_loc=settings.COMPILED_JS_LOC,
                recurse=settings.INCLUDE_JS_RECURSIVELY)
        jsc.resolve_dependencies()
        js_files = [f.split(settings.MEDIA_ROOT)[-1] for f in jsc.file_list]
    else:
        js_files = [settings.COMPILED_JS_LOC.split(settings.MEDIA_ROOT)[-1]]
    version = JSVersion.objects.get_or_create(pk=1)[0].version
    resp = ''
    for f in js_files: 
        resp += '<script src="%s?version=%s"></script>' % (
                settings.MEDIA_URL+f[1:], str(version))
    return resp

