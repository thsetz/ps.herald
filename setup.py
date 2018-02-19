from setuptools import setup, find_packages
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
    	

install_requires=[
"flask",
"Flask-Bootstrap",
"Flask-HTTPAuth",
"Flask-Login",
"Flask-Mail",
"Flask-Migrate",
"Flask-Moment",
"Flask-PageDown",
"Flask-SQLAlchemy",
"Flask-Script",
"Flask-WTF",
"Jinja2",
"Mako",
"Markdown",
"MarkupSafe",
"SQLAlchemy",
"WTForms",
"Werkzeug",
"alembic",
"bleach",
"blinker",
"html5lib",
"trollius",
"itsdangerous",
"six",
"docopt",
"dominate",
"visitor",
"ps.basic>=0.2.66",
"requests",
"future",
"six",
]

VERSION = _read('VERSION.txt').strip()

here = os.path.abspath(os.path.dirname(__file__))
open(os.path.join(here,'src', 'ps','herald_package_version.py'), 'w').write('version = "%s"' % VERSION)

setup(name='ps.herald',
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
      namespace_packages=['ps', ],
      include_package_data=True,
      dependency_links=["https://vl-pypi.haufe-ep.de/ps/DEVELOPMENT",],
      zip_safe=False,
      install_requires=install_requires,
      entry_points = {
	'console_scripts': [
	'ps_neelix=ps.neelix:main',
	'ps_bridge=ps.bridge:main',
	'ps_herald=ps.herald:main',
	],
     },
      )
