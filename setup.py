from setuptools import setup, find_packages


setup(
    name="Idiot",
    version="0.1",
    author="snare & y011",
    author_email="snare@ho.ax",
    description=(""),
    license="MIT",
    keywords="idiot",
    url="https://github.com/snare/idiot",
    packages=find_packages(),
    app=['app.py'],
    options={'py2app': {
        'argv_emulation': True,
        'plist': {
            'LSUIElement': True,
        },
        'packages': ['rumps', 'idiot', 'scruffy', 'psutil', 'biplist', 'emoji'],
    }},
    setup_requires=['py2app'],
    install_requires=['rumps', 'scruffington>=0.3.3', 'psutil', 'biplist', 'emoji'],
    entry_points={
        'console_scripts': ['idiot=idiot:main']
    },
    dependency_links=['http://github.com/snare/rumps/tarball/master#egg=rumps'],
    zip_safe=False,
    package_data={
        'idiot': ['config/default.conf'],
    }
)
