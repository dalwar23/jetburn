#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup script

Make documentation with:
cd docs
make clean html
"""

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@protonmail.com"

# Import python libraries
import sys
from setuptools import setup, find_packages

# Check if enough parameter has been given to install or not
if sys.argv[-1] == "setup.py":
    print("To install, run 'python setup.py install'")

# Check python version before installing
if sys.version_info[:2] < (3, 6):
    print("jetburn docs require Python3.6 or later!")
    sys.exit(1)

# Get version and release for this package
package_name = "jetburn"
release_file = "version.py"
release_info = {}
with open(release_file, "rb") as rf:
    exec(rf.read(), release_info)


# Read the README.md file for long description
def readme():
    with open("README.rst") as f:
        return f.read()


# Standard boilerplate to run this script
if __name__ == "__main__":
    setup(
        name=package_name,
        version=release_info["__version__"],
        author=release_info["__author__"],
        author_email=release_info["__author_email__"],
        description="Airline ticket explorer program",
        keywords=["airline", "ticket"],
        long_description=readme(),
        license=release_info["__license__"],
        platforms=["Linux", "Mac OSX", "Windows", "Unix"],
        url="https://jetburn.rtfd.io",
        download_url="",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        packages=find_packages(),
        include_package_data=True,
        install_requires=["sphinx", "recommonmark", "sphinx_rtd_theme", "Pygments", "sphinx-copybutton"],
        zip_safe=False,
    )
