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


class UiInputForm(UiFormsMacro):
    tpl_name = 'inputform.tpl'

    def __new__(cls, options, styles=''):
        fields = []
        for i, k in enumerate(options.get('fields', [])):
            fields.append({
                'type': k.get('type', 'text'),
                'label': k.get('label', 'Field %s' % (i + 1)),
                'name': k.get('name', 'field_%s' % i),
                'value': k.get('value', ''),
                'format': k.get('format', ''),
                'options': k.get('options', []),
                'multiple': k.get('multiple', False),
                'rows': k.get('rows', 4),
                'placeholder': k.get('placeholder', k.get('label', '')),
                'required': k.get('required', False),
                'confirm': k.get('confirm', False),
                'help': k.get('help', ''),
                'helpguide': k.get('helpguide', ''),
                'prepend': k.get('prepend', []),
                'append': k.get('append', []),
            })
        return cls.tpl(**{
            'id': options.get('form_id', cls.randint()),
            'submit_url': options.get('submit_url', ''),
            'fields': fields,
            'styles': styles,
        })


class UiLoginForm(UiFormsMacro):
    tpl_name = 'loginform.tpl'

    def __new__(cls, options, styles=''):
        return cls.tpl(**{
            'id': options.get('form_id', cls.randint()),
            'submit_url': options.get('submit_url', ''),
            'authkey': options.get('authkey', ''),
            'styles': styles,
        })
