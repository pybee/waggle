#!/usr/bin/env python
import io
import re
from setuptools import setup, find_packages


with io.open('./waggle/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='waggle',
    version=version,
    description='Tools for a BeeKeeper worker drone to report status back to the hive.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://pybee.org/waggle',
    keywords=['beekeeper'],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'waggle = waggle.waggle:main',
        ]
    },
    install_requires=[
        'github3.py~=0.9.6',
        'boto3~=1.4.4',
        'awscli~=1.11.115',
    ],
    license='New BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    test_suite='tests'
)
