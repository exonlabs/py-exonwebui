# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import random
from flask import render_template

__all__ = []


class UiBaseMacro(str):

    # root path for templates
    root_path = 'webui/macros'

    # template file name
    tpl_name = ''

    def __new__(cls, **params):
        return cls.tpl(**params)

    @classmethod
    def tpl(cls, **params):
        return render_template(
            '%s/%s' % (cls.root_path, cls.tpl_name), **params) + '\n'

    @classmethod
    def randint(cls, index=10000):
        return random.randint(index, (index * 10) - 1)
