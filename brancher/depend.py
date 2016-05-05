import importlib
import tempfile
import subprocess
import os
import site

def install_pip():
    tmpdir = tempfile.gettempdir()
    pip_file = os.path.join(tempfile.gettempdir(), 'get-pip.py')
    src_link = 'https://bootstrap.pypa.io/get-pip.py'
    res = subprocess.call(['wget', src_link, '-O', pip_file])
    if res != 0:
        raise Exception('Error occurred while downloading pip')
    res = subprocess.call(['python', pip_file, '--user'])
    if res != 0:
        raise Exception('Error occurred while installing pip')

def check_pip():
    try:
        importlib.import_module('pip')
    except ImportError:
        install_pip()
        reload(site)
    finally:
        globals()['pip'] = importlib.import_module('pip')

def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

def check_dependencies():
    check_pip()
    dependencies = ['lxml', 'requests']
    for package in dependencies:
        install_and_import(package)
