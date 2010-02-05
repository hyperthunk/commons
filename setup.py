"""Installs badrabbit using distutils

Run:
    python setup.py install

to install this package.
"""

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
import sys
import os
import shutil

required_python_version = '2.3'

name = "commons"
version = "0.1.0"

def main():
    if sys.version < required_python_version:
        s = "I'm sorry, but %s %s requires Python %s or later."
        print s % (name, version, required_python_version)
        sys.exit(1)
    # set default location for "data_files" to
    # platform specific "site-packages" location
    for scheme in INSTALL_SCHEMES.values():
        scheme['data'] = scheme['purelib']
    
    dist = setup(
        name=name,
        version=version,
        description="Python Commons",
        long_description="Utility code.",
        author="Tim Watson",
        author_email="watson.timothy@gmail.com",
        url="http://github.com/n0gg1n/commons",
        license="BSD",
        packages=['commons'],
        download_url="http://github.com/n0gg1n/badrabbit",
        data_files=[('commons',['INSTALL', 'LICENSE', 'README'])]
    )


if __name__ == "__main__":
    main()
