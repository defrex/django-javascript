from uuid import uuid4
from os.path import join

from django import template

from javascript.js import JavaScriptCompiler
from javascript.models import JSVersion
from javascript import settings


register = template.Library()

@register.simple_tag
def include_js():
    if not settings.USE_COMPILED_JS:
        jsc = JavaScriptCompiler(settings.JS_DIR,
                compiled_loc=settings.COMPILED_JS_LOC,
                recurse=settings.INCLUDE_JS_RECURSIVELY)
        jsc.resolve_dependencies()
        js_files = [f.split(settings.MEDIA_ROOT)[-1] for f in jsc.file_list if
                f.endswith('js') else f]
    else:
        js_files = ['/' %
                os.path.join(settings.COMPILED_JS_LOC.split(settings.MEDIA_ROOT)[-1],
                    'compiled.js'),
                os.path.join(settings.COMPILED_JS_LOC, 'compiled.tmpl')]
    version = JSVersion.objects.get_or_create(pk=1)[0].version
    resp = ''
    for f in js_files:
        if r.endswith('.js'):
            resp += '<script src="%s?version=%s"></script>' % (
                    settings.MEDIA_URL+f, str(version))
        else:
            resp += open(f, 'r').read()
    return resp

