
from django import template

from javascript.js import JavaScriptCompiler
from javascript.models import JSVersion
from javascript import settings


register = template.Library()

@register.simple_tag
def include_js():
    if not settings.JS_USE_COMPILED:
        jsc = JavaScriptCompiler(settings.JS_DIR,
                compiled_loc=settings.JS_COMPILED_LOC,
                recurse=settings.JS_INCLUDE_RECURSIVELY)
        jsc.resolve_dependencies()
        js_files = [f.split(settings.JS_STATIC_ROOT)[-1] for f in jsc.file_list]
    else:
        js_files = ['/' + settings.JS_COMPILED_LOC.split(settings.JS_STATIC_ROOT)[-1]]
    version = JSVersion.objects.get_or_create(pk=1)[0].version
    resp = ''
    for f in js_files:
        resp += '<script src="%s?version=%s"></script>' % (
                settings.STATIC_URL + f, str(version))
    return resp
