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

    def __new__(cls, url, authkey, form_id=None, styles=''):
        return cls.tpl(**{
            'id': cls.randint() if form_id is None else form_id,
            'url': url,
            'authkey': authkey,
            'styles': styles,
        })
