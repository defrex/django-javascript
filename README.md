# django-javascript

This simple Django app is for managing JavaScript in a Django project. It provides a way to specify dependencies in JavaScript files, to include your JavaScript in a template ordered according to the dependencies, to compile your JavaScript using Google's [Closure Compiler](http://code.google.com/closure/compiler/), and to include that compiled JavaScript with a GET argument version for cache-busting.

## JavaScript dependencies

Generally when a site deals with a large amount of js there becomes a sacred set of `<script>` tags at the top of the base template that should not be fucked with for feat of un-ordering a somewhat fragile set of only semi-understood dependencies.

Including this line at the top of each js file should help that:

    //depends: main.js, utils.js, jquery.js

This comment should be the first line in the file, and can contain one or more dependency.

## Including JavaScript in a template

It's simple:

    {% load include_js %}
    {% include_js %}

This will do one of two things. If `DEBUG` is `True` (or `USE_COMPILED_JS` is `False`) it will include a bunch of `<script>` tags ordered appropriately. Otherwise, it will include one `<script>` tag, pointing to 'compiled.js' (or the file at `COMPILED_JS_LOC`). It will also append `?version={the number of times compile_js has been called}`

## Compiling

You may have noticed that I've been using the term "compiled" rather than "minified". This is because when the command is run, add the js files are dependency-resolved and concatinated into a single file, and _that_ file is minified. In my mind this is more like a compilation then a simple minification. But I guess it's just semantics.

When you're ready:

    python manage.py compile_js

This will create 'compiled.js' (or the file at `COMPILED_JS_LOC`), and will rev the cach-buster number.

## settings

One setting is required: `JS_DIR`. It should be the full path to the directory where all the js files are. Here are all of the settings available though:

    JS_DIR = '' # must be set
    # This is stripped off the file's path and replaced with STATIC_URL
    JS_STATIC_ROOT = settings.STATIC_ROOT
    JS_USE_COMPILED = not DEBUG
    JS_COMPILED_LOC = os.path.join(JS_DIR, 'compiled.js')
    JS_COMPILATION_LEVEL = 'SIMPLE_OPTIMIZATIONS' # use 'ADVANCED_OPTIMIZATIONS' if your hardcore.
    JS_INCLUDE_RECURSIVELY = True # False is handy if there is some js you don't want compiled

See more about [Closure Compiler compilation levels](http://code.google.com/closure/compiler/docs/compilation_levels.html).

