import os
import shutil
import sys
import zipfile
import platform

from distutils.core import setup
import py2exe
import glob

def find_data_files(source,target,patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())

version = __import__('p2pool').__version__
im64 = '64' in platform.architecture()[0]

if os.path.exists('INITBAK'):
    os.remove('INITBAK')
os.rename(os.path.join('p2pool', '__init__.py'), 'INITBAK')
try:
    open(os.path.join('p2pool', '__init__.py'), 'wb').write('__version__ = %r%s%sDEBUG = False%s' % (version, os.linesep, os.linesep, os.linesep))
    bundle = 1
    if im64:
        bundle = bundle + 2
    sys.argv[1:] = ['py2exe']
    setup(name='p2pool',
        version=version,
        description='Peer-to-peer Bitcoin mining pool',
        author='Forrest Voight',
        author_email='forrest@forre.st',
        url='http://p2pool.forre.st/',
        data_files=find_data_files('web-static','web-static',"*"),
   
        console=['run_p2pool.py'],
        options=dict(py2exe=dict(
            bundle_files=bundle,
            dll_excludes=['w9xpopen.exe', "mswsock.dll", "MSWSOCK.dll"],
            includes=['twisted.web.resource', 'yac_scrypt'],
            packages=['zope.interface']
        )),
        zipfile=None,
    )
finally:
    os.remove(os.path.join('p2pool', '__init__.py'))
    os.rename('INITBAK', os.path.join('p2pool', '__init__.py'))

win = '32'
if im64:
    win = '64'
    
dir_name = 'p2pool_win' + win + '_' + version

if os.path.exists(dir_name):
    shutil.rmtree(dir_name)
os.rename('dist', dir_name)

with zipfile.ZipFile(dir_name + '.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for dirpath, dirnames, filenames in os.walk(dir_name):
        for filename in filenames:
            zf.write(os.path.join(dirpath, filename))

print dir_name
