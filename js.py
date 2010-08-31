import os
from os.path import join, isfile, abspath, isdir, dirname
import tempfile
from subprocess import Popen

from javascript import settings

class GoogleClosureMinifier(object):
    
    def __init__(self, jar_loc):
        self.jar_loc = jar_loc
    
    def assign_values(self, js, output_location):
        self.js = js
        self.output_location = output_location
    
    def minify(self):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(str(self.js))
        tmp.close()
        command = 'java -jar %(jar)s --compilation_level %(level)s --js %(tmp_loc)s --js_output_file %(output_loc)s' % {
            'jar': self.jar_loc,
            'level': settings.JS_COMPILATION_LEVEL,
            'tmp_loc': tmp.name,
            'output_loc': self.output_location,
        }
        p = Popen(command, shell=True)
        retcode = p.wait()
        os.remove(tmp.name)

class DummyMinifier(object):
    
    def assign_values(self, js, output_location):
        self.js = js
        self.output_location = output_location
    
    def minify(self):
        with open(self.output_location, 'w+') as f:
            f.write(self.js)


class JavaScriptCompiler(object):
    directory = None
    file_list = None
    file_list_resolved = False
    concated_js = None
    compiled_js = None
    output_location = None
    
    def __init__(self, directory, minifier=None, compiled_loc=None, v=False,
                recurse=True):
        if not isdir(directory):
            raise AttributeError, 'JavaScriptCompiler object must be passed a valid directory'
        self.directory = abspath(directory)
        self.output_location = compiled_loc
        self.minifier = minifier
        self.v = v
        self.recurse = recurse
    
    def make_file_list(self):
        if self.file_list is not None:
            return self.file_list
        
        if self.v: print 'Making file list...'
        
        files = list()
        def search_dir(directory):
            for item in os.listdir(directory):
                if isdir(join(directory, item)) and self.recurse:
                    search_dir(join(directory, item))
                elif item.endswith('.js'):
                    if not self.output_location == join(directory, item):
                        files.append(join(directory, item))
        
        search_dir(self.directory)
        self.file_list = files
    
    def resolve_dependencies(self, search_depth=200):
        ''' 
        by pstein (mostly)
        
        Resolves the dependencies from a list of javascript files.
        
        Paths must be absolute.  Returns a sorted list of files, in order of
        inclusion.  If any dependencies cannot be met they will be printed to the
        command line and ignored.
        
        The method used to detect circular dependencies is a simple cap on the
        number of iterations allowed; as such, complex dependencies between a 
        large list of files may not resolve completely.  If this happens, setting
        the maximum iterations argument to a value higher than the default will
        help.
        '''
        if self.file_list is None:
            self.make_file_list()
        
        if self.v: print 'Resolving file dependancies...'
        
        js_files = self.file_list[:]
        output = list()
        js_added = 0
        cur_depth = 0
        
        #The algorithm is rather simple: run through the list of files, removing
        #any file who's dependencies are fully met.  We count and limit the number
        #of runs through the list in order to prevent circular dependencies from
        #sticking us into an infinite loop.
        
        #keep going as long as we haven't resolved all the files and we haven't
        #hit the run cap
        while js_added < len(self.file_list) and cur_depth < search_depth:
            for f in js_files:
                #grab the first line of the file
                f = open(f, 'r')
                deps = f.readline()
                f.close()
                f = f.name
                #if the file has dependencies, see if they're resolved
                if deps.startswith('//depends:'):
                    dep_files = deps[10:].rstrip('\n').split(',')
                    found = False 
                    for dep in [dep.strip() for dep in dep_files]:
                        found = False
                        for item in output:
                            short_name = item.split(self.directory)[-1].lstrip('/')
                            if short_name == dep:
                                found = True
                                break
                        if not found:
                            break
                    if not found:
                        continue
                
                #all deps are met
                js_files.remove(f)
                output.append(f)
                js_added += 1
                break #break, since we modified the array we're iterating over
                
            #increment the run count
            cur_depth += 1
        
        #if we hit the run limit, print the unresolved files
        if cur_depth == search_depth:
            print 'Unable to resolve dependencies for the following files:'
            for f in js_files:
                print '    %s' % f
        
        self.file_list_resolved = True
        self.file_list = output
    
    def concat_files(self):
        if self.file_list is None or not self.file_list_resolved:
            self.resolve_dependencies()
        
        if self.v: print 'Concating resolved files...'
        
        concated_js = ''
        for f in self.file_list:
            concated_js += open(f, 'r').read() + '\n'
        
        self.concated_js = concated_js
    
    def compile_js(self):
        if self.concated_js is None:
            self.concat_files()
        
        if self.v: print 'Minifing concated js...'
        
        if self.minifier is None:
            raise AttributeError, 'cannot compile without a minifier'
        if self.output_location is None:
            raise AttributeError, 'cannot compile without an output_location'
        
        self.minifier.assign_values(self.concated_js, self.output_location)
        self.minifier.minify()
        
        if self.v: print 'Compilation complete.'


def compile():
    minifier = GoogleClosureMinifier(settings.CLOSURE_JAR)
    jsc = JavaScriptCompiler(settings.JS_DIR, minifier,
            compiled_loc=settings.COMPILED_JS_LOC, v=True)
    jsc.compile_js()

if __name__ == "__main__": compile




