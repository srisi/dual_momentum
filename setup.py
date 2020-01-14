"""
Setup script for dual_momentum installation
"""
import sys
import setuptools

with open('requirements.txt') as f:
    REQUIRED_PACKAGES = f.read().strip().split('\n')

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

# Check if Python 3.6 or 3.7 is installed.
PYTHON_VERSION = sys.version_info
if PYTHON_VERSION.major < 3 or (PYTHON_VERSION.major == 3 and PYTHON_VERSION.minor < 6):
    ERR = ('gender_novels only supports Python Versions 3.6 and 3.7. '
           + 'Your current Python version is {0}.{1}.'.format(
               str(PYTHON_VERSION.major),
               str(PYTHON_VERSION.minor)
           ))
    sys.exit(ERR)

setuptools.setup(
    name="dual-momentum",
    version="0.1.0",
    author="Stephan Risi",
    install_requires=REQUIRED_PACKAGES,
    long_description=LONG_DESCRIPTION,
    packages=setuptools.find_packages(),
)
