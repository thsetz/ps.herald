from setuptools import setup
#install_requires=["flask","jinja2","ps.basic","sqlalchemy"]
install_requires=["Flask", "click", "flask-sqlalchemy", "ps.basic"],
version='1.1.0'

setup(
    name="ps.herald",
    version=version,
    long_description=open("README.rst").read() + "\n" ,
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: GPL',
          'Operating System :: MacOS',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development',
          'Topic :: Utilities',
      ], 
    keywords='PS',
    author='Setz',
    url='https://bitbucket.org/drsetz/ps.herald',
    author_email='Thomas.Setz@acm.org',
    license='GPL', 
    packages=["ps.herald"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "ps_neelix=ps.herald.ps_neelix:main",
            "ps_bridge=ps.herald.ps_bridge:main",
            "ps_herald=ps.herald.ps_herald:main",
        ],
    },
)
