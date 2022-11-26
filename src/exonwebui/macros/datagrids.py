# -*- coding: utf-8 -*-
import json
from . import UiBaseMacro

__all__ = []


class UiDataGridsMacro(UiBaseMacro):
    root_path = 'webui/macros/datagrids'


class UiStdDataGrid(UiDataGridsMacro):
    tpl_name = 'stddatagrid.min.j2'

    std_render = {'_': '_', 'display': 'd'}

    def __new__(cls, options, styles=''):
        columns = []
        for k in options.get('columns', []):
            columns.append(json.dumps({
                'name': k['id'],
                'title': k['title'],
                'data': k.get('data', k['id']),
                'render': k.get('render', cls.std_render),
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
            'cdn_url': options.get('cdn_url') or '',
            'lenMenu': options.get('length_menu', [25, 50, 100, -1]),
            'columns': ','.join(columns),
            'order': json.dumps(options.get('order', [2, 'asc'])),
            'single_ops': options.get('single_ops', []),
            'group_ops': options.get('group_ops', []),
            'export': export,
            'styles': styles,
            'jscript': options.get('jscript', ''),
        })

    @classmethod
    def text(cls, value, default='-', styles='', render=None):
        if not render or type(render) is not dict:
            render = cls.std_render
        return {
            render.get('_', '_'): value,
            render.get('display', 'd'):
                ('<div class="%s">%s</div>' % (styles, value))
                if value is not None else (
                    '<span class="text-black-50">%s</span>' % default),
        }

    @classmethod
    def password(cls, has_value, default='-', styles='', render=None):
        if not render or type(render) is not dict:
            render = cls.std_render
        return {
            render.get('_', '_'): '*****' if has_value else '',
            render.get('display', 'd'):
                ('<div class="%s">*****</div>' % (styles))
                if has_value else (
                    '<span class="text-black-50">%s</span>' % default),
        }

    @classmethod
    def link(cls, value, url, label=None, styles='', render=None):
        if not render or type(render) is not dict:
            render = cls.std_render
        return {
            render.get('_', '_'): value,
            render.get('display', 'd'):
                '<div class="%s"><a class="text-primary" href="%s">%s</a></div>'  # noqa
                % (styles, url, value if label is None else label),
        }

    @classmethod
    def pill(cls, value, true_chk, styles='', render=None):
        if not render or type(render) is not dict:
            render = cls.std_render
        return {
            render.get('_', '_'): value,
            render.get('display', 'd'):
                '<span class="badge badge-%s %s">%s</span>' % (
                    'success' if value == true_chk else 'danger',
                    styles, value),
        }

    @classmethod
    def icon(cls, value, icon, styles='', render=None):
        if type(icon) is dict:
            _icon = icon.get(value, '')
        else:
            _icon = icon
        if not render or type(render) is not dict:
            render = cls.std_render
        return {
            render.get('_', '_'): value,
            render.get('display', 'd'):
                '<span class="%s"><i class="fa fas fa-fw %s"></i></span>'
                % (styles, _icon),
        }

    @classmethod
    def check(cls, value, styles='', render=None):
        if not render or type(render) is not dict:
            render = cls.std_render
        return {
            render.get('_', '_'): value,
            render.get('display', 'd'):
                '<span class="%s %s"><i class="fa fas fa-fw %s"></i></span>'
                % ('text-success' if value else 'text-danger', styles,
                   'fa-check' if value else 'fa-times'),
        }

    @classmethod
    def datetime(cls, value, fmt='%Y-%m-%d %H:%M:%S', render=None):
        if not render or type(render) is not dict:
            render = cls.std_render
        return {
            render.get('_', '_'): value,
            render.get('display', 'd'):
                value.strftime(fmt) if value else '-',
        }

    @classmethod
    def date(cls, value, fmt='%Y-%m-%d', render=None):
        if not render or type(render) is not dict:
            render = cls.std_render
        return {
            render.get('_', '_'): value,
            render.get('display', 'd'):
                value.strftime(fmt) if value else '-',
        }

    @classmethod
    def time(cls, value, fmt='%H:%M:%S', render=None):
        if not render or type(render) is not dict:
            render = cls.std_render
        return {
            render.get('_', '_'): value,
            render.get('display', 'd'):
                value.strftime(fmt) if value else '-',
        }
