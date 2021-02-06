from setuptools import setup

setup(
    name="ps_herald",
    version="1.0",
    long_description=__doc__,
    packages=["ps.herald"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=["Flask", "click", "flask-sqlalchemy", "ps.basic"],
    entry_points={
        "console_scripts": [
            "ps_neelix=ps.herald.ps_neelix:main",
            "ps_bridge=ps.herald.ps_bridge:main",
            "ps_herald=ps.herald.ps_herald:main",
        ],
    },
)
