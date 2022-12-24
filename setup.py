# -*- coding: utf-8 -*-
import os
from setuptools import setup

os.chdir(os.path.abspath(os.path.dirname(__file__)))

setup(
    name="exonwebui",
    install_requires=[
        'exonutils>=7.0,<8.0',
    ],
)
