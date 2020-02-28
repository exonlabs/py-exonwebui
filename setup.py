# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup

os.chdir(os.path.abspath(os.path.dirname(__file__)))

__PKGNAME__ = 'exonwebui'
__VERSION__ = '0.1.dev'


setup(
    name=__PKGNAME__,
    version=__VERSION__,
    license='BSD',
    url='https://bitbucket.org/exonlabs/exonwebui',
    author='exonlabs',
    description='Web libraries for UI web applications.',
    packages=[__PKGNAME__],
    include_package_data=True,
    zip_safe=False,
    platforms='linux',
    python_requires='>=3.5',
    install_requires=[
        'exonutils>=1.0',
        'flask-seasurf>=0.2.2',
        'flask-babelex>=0.9.4',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
