from setuptools import setup, find_packages, find_namespace_packages
import os
import sys
import subprocess


def _read(name):
	    def appendnl(s):
	        if not s or s[-1] != '\n':
	            return s + '\n'
	        else:
	            return s
	
	    with open(name) as f:
	        return appendnl(f.read())

#if False: pass
#elif  "install" or "develop" in sys.argv:
#    result = subprocess.call("pip install -r requirements/common.txt ", shell=True)
#    if result != 0:
#        sys.stdout.write("Not quite shure what to do here")
    	

#open("requirements.tyt").read().decode('utf-8').split()
install_requires= open("requirements.txt").read().split()  

VERSION = _read('VERSION.txt').strip()

here = os.path.abspath(os.path.dirname(__file__))
open(os.path.join(here,'src', 'ps_herald','herald_package_version.py'), 'w').write('version = "%s"' % VERSION)

print(find_packages('src'))
print(find_namespace_packages(where='src'))

setup(name='ps_herald',
      version=VERSION,
      description="Monitoring in the PS environment",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join( "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='PS',
      author='Setz',
      url='www.setz.de',
      author_email='Thomas.Setz@haufe-lexware.com',
      license='', # need/want 'ZPL'?
      packages=find_packages('src'),
      package_dir={'':'src'},
      #namespace_packages=['ps' ],
      #namespace_packages=find_namespace_packages(where='src'),
      include_package_data=True,
      dependency_links=["https://vl-pypi.haufe-ep.de/ps/DEVELOPMENT",],
      zip_safe=False,
      install_requires=install_requires,
      entry_points = {
	'console_scripts': [
	'ps_neelix=ps_herald.ps_neelix:main',
	'ps_bridge=ps_herald.ps_bridge:main',
	'ps_herald=ps_herald.ps_herald:main',
	],
     },
      )
