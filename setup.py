# -*- coding: utf-8 -*-
import os
from setuptools import setup

os.chdir(os.path.abspath(os.path.dirname(__file__)))

setup(
    name="exonwebui",
    install_requires=[
        'flask>=2.0,<3.0',
        'Werkzeug>=2.0,<3.0',
        'exonutils>=7.0,<8.0',
        'pytz',
    ],
)
