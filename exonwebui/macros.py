# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from flask import render_template


class Macro(object):

    base_path = 'webui/macros'

    @classmethod
    def load(cls, name, params):
        return render_template(
            '%s/%s.tpl' % (cls.base_path, name), **params)

    @classmethod
    def alert(cls, category, message, dismissible=False, styles=''):
        params = {
            'category': category,
            'message': message,
            'dismissible': dismissible,
            'styles': styles,
        }
        return cls.load('alert', params)

    @classmethod
    def loginform(cls, url, authkey, styles=''):
        params = {
            'url': url,
            'authkey': authkey,
            'styles': styles,
        }
        return cls.load('loginform', params)
