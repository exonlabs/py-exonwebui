# -*- coding: utf-8 -*-
"""
    :copyright: 2021, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from . import UiBaseMacro

__all__ = []


class UiBasicMacro(UiBaseMacro):
    root_path = 'webui/macros/basic'


class UiAlert(UiBasicMacro):
    tpl_name = 'alert.tpl'

    def __new__(cls, type, msg, icon=True, dismiss=True, styles=''):
        if type == 'error':
            alert_type, alert_icon = 'danger', 'fa-exclamation-circle'
        elif type == 'warn':
            alert_type, alert_icon = 'warning', 'fa-exclamation-circle'
        elif type == 'info':
            alert_type, alert_icon = 'info', 'fa-info-circle'
        elif type == 'success':
            alert_type, alert_icon = 'success', 'fa-check-circle'
        else:
            alert_type, alert_icon = 'secondary', ''
        if not icon:
            alert_icon = ''

        return cls.tpl(**{
            'alert_type': alert_type,
            'alert_icon': alert_icon,
            'message': msg,
            'dismissible': dismiss,
            'styles': styles,
        })


class UiLinkModal(UiBasicMacro):
    tpl_name = 'linkmodal.tpl'

    def __new__(cls, caption, title, contents, styles=''):
        return cls.tpl(**{
            'id': cls.randint(),
            'caption': caption,
            'title': title,
            'contents': contents,
            'styles': styles,
        })
