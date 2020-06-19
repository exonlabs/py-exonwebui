# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from . import UiBaseMacro

__all__ = []


class UiFormsMacro(UiBaseMacro):
    root_path = os.path.join('webui', 'macros', 'forms')


class UiLoginForm(UiFormsMacro):

    tpl_name = 'loginform.tpl'

    def __new__(cls, options, styles=''):
        return cls.tpl(**{
            'id': options.get('form_id', cls.randint()),
            'submit_url': options.get('submit_url', ''),
            'authkey': options.get('authkey', ''),
            'styles': styles,
        })
