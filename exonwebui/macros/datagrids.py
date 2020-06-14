# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import simplejson as json
from . import UiBaseMacro

__all__ = []


class UiDataGridsMacro(UiBaseMacro):
    root_path = os.path.join('webui', 'macros', 'datagrids')


class UiStdDataGrid(UiDataGridsMacro):

    tpl_name = 'stddatagrid.tpl'

    def __new__(cls, options, styles=''):
        columns = []
        for col in options.get('columns', []):
            columns.append(json.dumps({
                'name': col['id'],
                'data': col['id'],
                'title': col['title'],
                'type': col.get('coltype', col.get('type', 'string')),
                'visible': col.get('visible', True),
                'searchable': col.get('searchable', True),
                'orderable': col.get('orderable', True),
            }))
        return cls.tpl(**{
            'id': options.get('form_id', cls.randint()),
            'url': options.get('submit_url', ''),
            'title': options.get('title', '<i class="fas fa-list"></i>'),
            'lenMenu': options.get('lengthMenu', [25, 50, 100, -1]),
            'columns': ','.join(columns),
            'export_prefix': options.get('export_prefix', 'export'),
            'styles': styles,
        })
