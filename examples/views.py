# -*- coding: utf-8 -*-
import time
from random import randint
from flask import current_app, session, flash, request, \
    url_for, render_template as tpl
from flask_babelex import gettext, lazy_gettext

from exonutils.buffers.filebuffer import SimpleFileBuffer
from exonwebui.menuboard import MenuBoardView

# board menu buffer
MENU_BUFFER = {}


class Index(MenuBoardView):
    routes = [('/', 'index')]

    def initialize(self):
        global MENU_BUFFER
        self.add_menulink(
            MENU_BUFFER, 1,
            lazy_gettext('UI Components'), icon='fa-cubes')

    def get(self, **kwargs):
        global MENU_BUFFER

        params = {
            'doc_lang': session.get('lang', ''),
            'doc_langdir': session.get('lang_dir', ''),
            'doc_title': "WebUI",
            'cdn_url': current_app.config.get('TPL_CDN_URL'),
            'menu': MENU_BUFFER,
        }

        if not session.get('simpleboard', None):
            session['simpleboard'] = False
        if request.args.get('toogleboard', '').strip():
            session['simpleboard'] = not session['simpleboard']
            return self.redirect(url_for('index'))

        if session.get('simpleboard', False):
            return tpl('simpleboard.min.j2', **params)
        else:
            return tpl('mainboard.min.j2', **params)


class Home(MenuBoardView):
    routes = [('/home', 'home')]

    def initialize(self):
        global MENU_BUFFER
        self.add_menulink(
            MENU_BUFFER, 0,
            lazy_gettext('Home'), icon='fa-home', url='#home')

    def get(self, **kwargs):
        html = tpl('option_panel.min.j2', message=gettext("Welcome"))
        return self.reply(html, doctitle=gettext('Home'))


class Notify(MenuBoardView):
    routes = [('/notify', 'notify')]

    def initialize(self):
        global MENU_BUFFER
        self.add_menulink(
            MENU_BUFFER, 1,
            lazy_gettext('Notifications'), url='#notify', parent=1)

    def get(self, **kwargs):
        from exonwebui.macros.basic import UiAlert
        flash(gettext('error message') + " STICKY_MSG", 'error.us')
        flash(gettext('warning message'), 'warn')
        flash(gettext('info message'), 'info')
        flash(gettext('success message'), 'success')
        html = UiAlert('general message', gettext('showing notifications'),
                       styles='p-3', dismiss=False)
        return self.reply(html, doctitle=gettext('Notifications'))


class Alerts(MenuBoardView):
    routes = [('/alerts', 'alerts')]

    def initialize(self):
        global MENU_BUFFER
        self.add_menulink(
            MENU_BUFFER, 2,
            lazy_gettext('Alerts'), url='#alerts', parent=1)

    def get(self, **kwargs):
        from exonwebui.macros.basic import UiAlert
        html = UiAlert('info', gettext('info message'), styles='px-3 pt-3')
        html += UiAlert('warn', gettext('warning message'), styles='px-3')
        html += UiAlert('error', gettext('error message'), styles='px-3')
        html += UiAlert('success', gettext('success message'), styles='px-3')
        html += UiAlert('message', gettext('general message'), styles='px-3')
        return self.reply(html, doctitle=gettext('Alerts'))


class InputForm(MenuBoardView):
    routes = [('/inputform', 'inputform')]

    def initialize(self):
        global MENU_BUFFER
        self.add_menulink(
            MENU_BUFFER, 3,
            lazy_gettext('Input Form'), url='#inputform', parent=1)

    def get(self, **kwargs):
        from exonwebui.macros.forms import UiInputForm
        options = {
            'form_id': "1234",
            'submit_url': "/inputform",
            'cdn_url': current_app.config.get('TPL_CDN_URL'),
            'fields': [
                {'type': 'checkbox', 'label': gettext('Validation'),
                 'options': [{'label': gettext('Server side validation'),
                              'name': 'validation'}]},

                {'type': 'title', 'label': gettext('Group Label')},
                {'type': 'text', 'label': gettext('Required Field'),
                 'name': 'field1', 'required': True,
                 'help': gettext("* example with input append"),
                 'helpguide': gettext("Extra detailed long help for fields"),
                 'append': [{'type': 'text', 'value': '.00'},
                            {'type': 'text', 'value': '$'}]},
                {'type': 'text', 'label': gettext('Optional Field'),
                 'name': 'field2', 'required': False,
                 'help': gettext("* example with input prepend"),
                 'helpguide': gettext("Extra detailed long help for fields"),
                 'prepend': [{'type': 'icon', 'value': 'fa-phone'},
                             {'type': 'text', 'value': '+00'}]},
                {'type': 'text', 'label': gettext('Optional Field'),
                 'name': 'field3', 'required': False,
                 'help': gettext("* help text for field"),
                 'helpguide': gettext("Extra detailed long help for fields"),
                 'append': [{'type': 'select', 'options': [
                            {'label': '.com', 'value': '.com'},
                            {'label': '.net', 'value': '.net',
                             'selected': True},
                            {'label': '.org', 'value': '.org'}]}]},
                {'type': 'textarea', 'label': gettext('Textarea'),
                 'name': 'field4',
                 'help': gettext("* help text for field"),
                 'helpguide': gettext("Extra detailed long help for fields")},

                {'type': 'title', 'label': gettext('Group Label')},
                {'type': 'password', 'label': gettext('Password 1'),
                 'name': 'pass1', 'required': True, 'strength': True},
                {'type': 'password', 'label': gettext('Password 2'),
                 'name': 'pass2', 'required': True, 'confirm': True},
                {'type': 'password', 'label': gettext('Password 3'),
                 'name': 'pass3', 'required': True, 'strength': True,
                 'confirm': True},

                {'type': 'title', 'label': gettext('Group Label')},
                {'type': 'select', 'label': gettext('Select'),
                 'name': 'select1', 'required': True,
                 'options': [{'label': gettext('Select'), 'value': None},
                             {'label': gettext('Option 1'), 'value': '01'},
                             {'label': gettext('Option 2'), 'value': '02'},
                             {'label': gettext('Option 3'), 'value': '03'},
                             {'label': gettext('Option 4'), 'value': '04'},
                             {'label': gettext('Option 5'), 'value': '05'}]},
                {'type': 'select', 'label': gettext('Select multiple'),
                 'name': 'select2', 'required': True, 'multiple': True,
                 'options': [{'label': gettext('Option 1'), 'value': '01',
                              'selected': True},
                             {'label': gettext('Option 2'), 'value': '02',
                              'selected': True},
                             {'label': gettext('Option 3'), 'value': '03'},
                             {'label': gettext('Option 4'), 'value': '04'},
                             {'label': gettext('Option 5'), 'value': '05'}]},

                {'type': 'title', 'label': gettext('Group Label')},
                {'type': 'checkbox', 'label': gettext('Checkbox'),
                 'helpguide': gettext("Extra detailed long help for fields"),
                 'options': [{'label': gettext('Select 1'),
                              'name': 'check1', 'selected': True},
                             {'label': gettext('Select 2'),
                              'name': 'check2'}]},
                {'type': 'radio', 'label': gettext('Radio'),
                 'name': 'radio1', 'required': True,
                 'helpguide': gettext("Extra detailed long help for fields"),
                 'options': [{'label': gettext('Option 1'), 'value': '1'},
                             {'label': gettext('Option 2'), 'value': '2'},
                             {'label': gettext('Option 3'), 'value': '3'}]},

                {'type': 'title', 'label': gettext('Group Label')},
                {'type': 'datetime', 'label': gettext('Date & Time'),
                 'name': 'date1', 'required': True},
                {'type': 'date', 'label': gettext('Date'), 'name': 'date2'},
                {'type': 'time', 'label': gettext('Time'), 'name': 'time1'},

                {'type': 'title', 'label': gettext('Group Label')},
                {'type': 'file', 'label': gettext('Upload File'),
                 'name': 'files1', 'required': True,
                 'format': '.txt,.pdf,.png',
                 'help': '* %s: <span dir="ltr">.txt, .pdf, .png</span>'
                    % gettext("allowed types")},
                {'type': 'file', 'label': gettext('Upload Multiple'),
                 'name': 'files2', 'required': False, 'multiple': True,
                 'placeholder': '', 'maxsize': 1048576,
                 'help': gettext("* all types allowed, max file size: 1MB"),
                 'helpguide': gettext("Extra detailed long help for fields")},
            ]
        }
        html = tpl('input_form.min.j2', contents=UiInputForm(options))
        return self.reply(html, doctitle=gettext('Input Form'))

    def post(self, **kwargs):
        validation = request.form.get('validation', '')
        if validation == '1':
            params = {
                'validation': ['field1', 'date1', 'files1'],
            }
            flash(gettext('Please correct invalid fields'), 'error')
            return self.reply(None, **params)

        msg = '%s<br><div dir="ltr" style="text-align:left">' \
            % gettext('Submited Data:')
        for k in request.form.keys():
            if k == '_csrf_token':
                continue
            v = request.form.getlist(k)
            msg += "<b>%s:</b> %s<br>" % (k, v[0] if len(v) == 1 else v)
        for k in request.files.keys():
            v = [(f.filename, f.content_type)
                 for f in request.files.getlist(k) if f.filename]
            msg += "<b>%s:</b> %s<br>" % (k, v[0] if len(v) == 1 else v)
        msg += '</div>'
        msg = msg.replace("'", "")
        return self.notify(msg, 'success', sticky=True)


class Datagrid(MenuBoardView):
    routes = [('/datagrid', 'datagrid'),
              ('/datagrid/<action>', 'datagrid_1')]

    def initialize(self):
        global MENU_BUFFER
        self.add_menulink(
            MENU_BUFFER, 4,
            lazy_gettext('Datagrid'), url='#datagrid', parent=1)

    def get(self, **kwargs):
        from exonwebui.macros.datagrids import UiStdDataGrid
        options = {
            'grid_id': "1234",
            'base_url': "/datagrid",
            'load_url': "/datagrid/loaddata",
            'cdn_url': current_app.config.get('TPL_CDN_URL'),
            'length_menu': [10, 50, 100, 250, -1],
            'columns': [
                {'id': 'field1', 'title': "Field Name 1"},
                {'id': 'field2', 'title': "Field Name 2"},
                {'id': 'field3.item1', 'title': "Field3_1"},
                {'id': 'field3.item2', 'title': "Field3_2"},
                {'id': 'field4', 'title': "Other Field 4"},
                {'id': 'field5', 'title': "Extra Field 5",
                 'visible': False},
                {'id': 'field6', 'title': "Data Field 6",
                 'visible': False},
                {'id': 'field7', 'title': "Field Header 7",
                 'visible': False},
                {'id': 'field8', 'title': "Field8",
                 'visible': False},
                {'id': 'field9', 'title': "Field Number 9",
                 'visible': False},
            ],
            'export': {
                'types': ['csv', 'xls', 'print'],
                'file_title': "Example Data",
                'file_prefix': "export",
                'csv_fieldSeparator': ";",
                'csv_fieldBoundary': '',
            },
            'single_ops': [
                {'label': 'Single Operation 1', 'action': "single_op1"},
                {'label': 'Single Op 2 with confirm', 'action': "single_op2",
                 'confirm': 'Are you sure you want to do this operation?'},
            ],
            'group_ops': [
                {'label': 'Group Operation 1', 'action': "group_op1"},
                {'label': 'Group Op 2 with confirm', 'action': "group_op2",
                 'confirm': 'Are you sure?'},
                {'label': 'Op 3 with Reload', 'action': "group_op3"},
            ],
        }
        html = tpl('data_grid.min.j2', contents=UiStdDataGrid(options))
        return self.reply(html, doctitle=gettext('Datagrid'))

    def post(self, **kwargs):
        from exonwebui.macros.datagrids import UiStdDataGrid

        action = kwargs.get('action') or ''

        if action == 'loaddata':
            data = []
            for k in range(228):
                _k = str(k).rjust(3, '0')
                data.append({
                    'DT_RowId': 'rowid_%s' % _k,
                    'field1': UiStdDataGrid.link(
                        'master_%s' % _k, '#datagrid'),
                    'field2': UiStdDataGrid.text(
                        'field2 %s' % _k),
                    'field3': {
                        'item1': UiStdDataGrid.text(
                            'field3.1 %s' % _k if randint(0, 2) else ''),
                        'item2': UiStdDataGrid.text(
                            'field3.2 %s' % _k if randint(0, 3) else ''),
                    },
                    'field4': UiStdDataGrid.pill(
                        'Yes' if randint(0, 1) else 'No', 'Yes'),
                    'field5': UiStdDataGrid.check(
                        bool(randint(0, 1))),
                    'field6': UiStdDataGrid.text(
                        'field6 %s' % _k if randint(0, 1) else ''),
                    'field7': UiStdDataGrid.text(
                        'field7 %s' % _k if randint(0, 1) else ''),
                    'field8': UiStdDataGrid.text(
                        'field8 %s' % _k if randint(0, 1) else ''),
                    'field9': UiStdDataGrid.text(
                        'field9 %s' % _k if randint(0, 1) else ''),
                })
            return self.reply(data)

        if action in ['single_op1', 'single_op2',
                      'group_op1', 'group_op2', 'group_op3']:
            rows = request.form.getlist('items[]')
            if len(rows) > 20:
                rows = rows[:21]
                rows[20] = '...'
            msg = '<span dir="ltr" style="text-align:left">'
            msg += 'Operation: %s<br>' % action
            msg += 'Rows: %s' % rows
            msg += '</span>'
            msg = msg.replace("'", "")
            flash(msg, 'success.us')
            if action == 'group_op3':
                return self.reply(None, reload=True)
            else:
                return self.reply(None)

        return self.notify("Invalid request", 'error')


class QueryBuilder(MenuBoardView):
    routes = [('/qbuilder', 'qbuilder')]

    def initialize(self):
        global MENU_BUFFER
        self.add_menulink(
            MENU_BUFFER, 5,
            lazy_gettext('Query Builder'), url='#qbuilder', parent=1)

    def get(self, **kwargs):
        from exonwebui.macros.forms import UiQBuilder
        options = {
            'form_id': "1234",
            'cdn_url': current_app.config.get('TPL_CDN_URL'),
            'filters': [
                {'id': 'field1', 'label': 'Field 1', 'type': 'string',
                 'operators': ['equal', 'not_equal', 'contains']},
                {'id': 'field2', 'label': 'Field Name 2', 'type': 'string',
                 'input': 'textarea'},
                {'id': 'field3_1', 'label': 'Integer 1', 'type': 'integer',
                 'input': 'text'},
                {'id': 'field3_2', 'label': 'Integer 2', 'type': 'integer',
                 'input': 'number'},
                {'id': 'field3_3', 'label': 'Double 1', 'type': 'double',
                 'input': 'number'},
                {'id': 'field4', 'label': 'Select', 'type': 'integer',
                 'input': 'select',
                 'values': {1: 'Option 1', 2: 'Option 2', 3: 'Option 3'},
                 'operators': ['equal', 'not_equal', 'in', 'not_in']},
                {'id': 'field5', 'label': 'Checkbox', 'type': 'integer',
                 'input': 'radio', 'values': [{1: 'Yes'}, {0: 'No'}],
                 'operators': ['equal']},
                {'id': 'field6', 'label': 'Choose', 'type': 'integer',
                 'input': 'checkbox',
                 'values': [{1: 'Opt 1'}, {2: 'Opt 2'}, {3: 'Opt 3'},
                            {4: 'Opt 4'}, {5: 'Opt 5'}]},
            ],
            'initial_rules': {
                'not': True,
                'condition': 'AND',
                'rules': [
                    {'id': 'field1', 'operator': 'equal', 'value': 'value'},
                    {'id': 'field3_2', 'operator': 'less', 'value': 10},
                    {
                        'condition': 'OR',
                        'rules': [
                            {'id': 'field1', 'operator': 'equal',
                             'value': 'value2'},
                            {'id': 'field6', 'operator': 'equal',
                             'value': 2},
                        ],
                    },
                    {
                        'not': True,
                        'condition': 'OR',
                        'rules': [
                            {'id': 'field4', 'operator': 'equal',
                             'value': 3},
                            {'id': 'field2', 'operator': 'not_equal',
                             'value': 'text value'},
                        ],
                    },

                ],
            },
        }
        html = tpl('query_builder.min.j2', contents=UiQBuilder(options))
        return self.reply(html, doctitle=gettext('Query Builder'))


class Loader(MenuBoardView):
    routes = [('/loader', 'loader')]
    shared_buffer = SimpleFileBuffer('SampleWebui_Loader')

    def initialize(self):
        global MENU_BUFFER
        self.add_menulink(
            MENU_BUFFER, 2,
            lazy_gettext('Page Loader'), url='#loader')

    def get(self, **kwargs):
        from exonwebui.macros.basic import UiAlert
        html = UiAlert('message', gettext('loaded after delay'),
                       styles='p-3', dismiss=False)
        html += tpl('progress_loader.min.j2')

        # simulate delay
        time.sleep(3)

        return self.reply(html, doctitle=gettext('Page Loader'))

    def post(self, **kwargs):
        # get loading progress status
        if request.form.get('get_progress', ''):
            res = self.shared_buffer.get('loader_progress', 0)
            return self.reply(res)

        # simulate long delay
        t = 5
        for i in range(t):
            try:
                self.shared_buffer.set('loader_progress', int(i * 100 / t))
            except Exception:
                pass
            time.sleep(1)

        flash(gettext('success'), 'success')
        return self.reply(None)


class Loginpage(MenuBoardView):
    routes = [('/loginpage', 'loginpage'),
              ('/loginpage/<action>', 'loginpage_1')]

    def initialize(self):
        global MENU_BUFFER
        self.add_menulink(
            MENU_BUFFER, 3,
            lazy_gettext('Login Page'), url='loginpage')

    def get(self, **kwargs):
        from exonwebui.macros.forms import UiLoginForm

        action = kwargs.get('action') or ''

        if action == 'load':
            html = UiLoginForm({
                'cdn_url': current_app.config.get('TPL_CDN_URL'),
                'submit_url': url_for('loginpage'),
                'authkey': '123456',
            }, styles="text-white bg-secondary")
            return self.reply(html, doctitle=gettext('Loginpage'))
        else:
            params = {
                'doc_lang': session.get('lang', ''),
                'doc_langdir': session.get('lang_dir', ''),
                'doc_title': "WebUI",
                'cdn_url': current_app.config.get('TPL_CDN_URL'),
                'load_url': "%s/load" % url_for('loginpage'),
            }
            return tpl('loginpage.min.j2', **params)

    def post(self, **kwargs):
        username = request.form.get('username', '')
        authdigest = request.form.get('digest', '')

        if not username or not authdigest:
            err = gettext("Please enter username and password")
        else:
            if username == 'admin':
                flash("%s: %s" % (gettext("Welcome"), username), 'info')
                return self.redirect(url_for('index'))
            else:
                err = gettext("Invalid username or password")

        return self.notify(err, 'error')
