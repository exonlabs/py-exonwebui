# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import json
from . import UiBaseMacro

__all__ = []


class UiDataGridsMacro(UiBaseMacro):
    root_path = 'webui/macros/datagrids'


class UiStdDataGrid(UiDataGridsMacro):
    tpl_name = 'stddatagrid.tpl'

    text_render = {'_': '_', 'display': 'd'}
    link_render = {'_': '_', 'display': 'd'}
    pill_render = {'_': '_', 'display': 'd'}
    icon_render = {'_': '_', 'display': 'd'}
    check_render = {'_': '_', 'display': 'd'}

    def __new__(cls, options, styles=''):
        columns = []
        for k in options.get('columns', []):
            columns.append(json.dumps({
                'name': k['id'],
                'title': k['title'],
                'data': k.get('data', k['id']),
                'render': k.get('render', None),
                'type': k.get('type', 'string'),
                'visible': k.get('visible', True),
                'searchable': k.get('searchable', True),
                'orderable': k.get('orderable', True),
            }))
        export = {
            'types': ['csv', 'xls', 'print'],
            'file_title': "",
            'file_prefix': "export",
            'csv_fieldSeparator': ',',
            'csv_fieldBoundary': '"',
            'csv_escapeChar': '"',
            'csv_extension': '.csv',
            'xls_sheetName': "Sheet1",
            'xls_extension': '.xlsx',
        }
        export.update(options.get('export', {}))
        return cls.tpl(**{
            'id': options.get('grid_id', cls.randint()),
            'baseurl': options.get('base_url', ''),
            'loadurl': options.get('load_url', ''),
            'lenMenu': options.get('length_menu', [25, 50, 100, -1]),
            'columns': ','.join(columns),
            'single_ops': options.get('single_ops', []),
            'group_ops': options.get('group_ops', []),
            'export': export,
            'styles': styles,
        })

    @classmethod
    def text(cls, value, default='-', styles=''):
        return {
            cls.text_render['_']: value,
            cls.text_render['display']:
                ('<span class="%s">%s</span>' % (styles, value))
                if value else (
                    '<span class="text-black-50">%s</span>' % default),
        }

    @classmethod
    def link(cls, value, url, label=None, styles=''):
        return {
            cls.link_render['_']: value,
            cls.link_render['display']:
                '<a class="text-primary %s" href="%s">%s</a>' % (
                    styles, url, value if label is None else label),
        }

    @classmethod
    def pill(cls, value, true_chk, styles=''):
        return {
            cls.pill_render['_']: value,
            cls.pill_render['display']:
                '<span class="badge badge-%s %s">%s</span>' % (
                    'success' if value == true_chk else 'danger',
                    styles, value),
        }

    @classmethod
    def icon(cls, value, icon, styles=''):
        if type(icon) is dict:
            _icon = icon.get(value, '')
        else:
            _icon = icon
        return {
            cls.icon_render['_']: value,
            cls.icon_render['display']:
                '<span class="%s"><i class="fa fas fa-fw %s"></i></span>'
                % (styles, _icon),
        }

    @classmethod
    def check(cls, value, styles=''):
        return {
            cls.check_render['_']: value,
            cls.check_render['display']:
                '<span class="%s %s"><i class="fa fas fa-fw %s"></i></span>'
                % ('text-success' if value else 'text-danger', styles,
                   'fa-check' if value else 'fa-times'),
        }
