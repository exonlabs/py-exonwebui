# -*- coding: utf-8 -*-
import os
import time
from random import randint
from flask import session, flash, request, url_for, render_template as tpl
from flask_babelex import gettext, lazy_gettext

from exonwebui.menuboard import MenuBoardView


class VIndex(MenuBoardView):
    routes = [('/', 'index')]

    @classmethod
    def initialize(cls, websrv, app):
        # disable strict slash matching
        app.url_map.strict_slashes = False

        # adjust session and csrf cookies attrs
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        app.config['CSRF_COOKIE_HTTPONLY'] = True
        app.config['CSRF_COOKIE_SAMESITE'] = 'Lax'
        app.config['CSRF_DISABLE'] = True

        # initialize board
        locale_path = os.path.join(websrv.base_path, 'locale')
        cls.board_initialize(app, locale_path=locale_path)

        # add menu section
        cls.add_menulink(
            app, 1, lazy_gettext('UI Components'), icon='fa-cubes')

    def get(self, **kwargs):
        params = {
            'doc_lang': session.get('lang', ''),
            'doc_langdir': session.get('lang_dir', ''),
            'doc_title': "WebUI",
        }

        if not session.get('simpleboard', None):
            session['simpleboard'] = False
        if request.args.get('toogleboard', '').strip():
            session['simpleboard'] = not session['simpleboard']
            return self.redirect(url_for('index'))

        if session.get('simpleboard', False):
            return self.reply(tpl('simpleboard.tpl', **params))
        else:
            return self.reply(tpl('mainboard.tpl', **params))


class VHome(MenuBoardView):
    routes = [('/home', 'home')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 0, lazy_gettext('Home'), icon='fa-home', url='#home')

    def get(self, **kwargs):
        html = tpl('option_panel.tpl', message=gettext("Welcome"))
        return self.reply(html, doctitle=gettext('Home'))


class VNotify(MenuBoardView):
    routes = [('/notify', 'notify')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 1, lazy_gettext('Notifications'), url='#notify', parent=1)

    def get(self, **kwargs):
        from exonwebui.macros.basic import UiAlert
        flash(gettext('error') + " STICKY_MSG", 'error.us')
        flash(gettext('warning'), 'warn')
        flash(gettext('info'), 'info')
        flash(gettext('success'), 'success')
        html = UiAlert('message', gettext('showing notifications'),
                       styles='p-3', dismiss=False)
        return self.reply(html, doctitle=gettext('Notifications'))


class VAlerts(MenuBoardView):
    routes = [('/alerts', 'alerts')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 2, lazy_gettext('Alerts'), url='#alerts', parent=1)

    def get(self, **kwargs):
        from exonwebui.macros.basic import UiAlert
        html = UiAlert('info', gettext('info'), styles='px-3 pt-3')
        html += UiAlert('warn', gettext('warning'), styles='px-3')
        html += UiAlert('error', gettext('error'), styles='px-3')
        html += UiAlert('success', gettext('success'), styles='px-3')
        html += UiAlert('message', gettext('message'), styles='px-3')
        return self.reply(html, doctitle=gettext('Alerts'))


class VInputForm(MenuBoardView):
    routes = [('/inputform', 'inputform')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 3, lazy_gettext('Input Form'), url='#inputform', parent=1)

    def get(self, **kwargs):
        from exonwebui.macros.forms import UiInputForm
        options = {
            'form_id': "1234",
            'submit_url': "/inputform",
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
        html = tpl('input_form.tpl', contents=UiInputForm(options))
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


class VDatagrid(MenuBoardView):
    routes = [('/datagrid', 'datagrid'),
              ('/datagrid/<action>', 'datagrid_1')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 4, lazy_gettext('Datagrid'), url='#datagrid', parent=1)

    def get(self, **kwargs):
        from exonwebui.macros.datagrids import UiStdDataGrid
        options = {
            'grid_id': "1234",
            'base_url': "/datagrid",
            'length_menu': [10, 50, 100, 250, -1],
            'columns': [
                {'id': 'field1', 'title': "Field Name 1",
                 'render': UiStdDataGrid.link_render},
                {'id': 'field2', 'title': "Field Name 2"},
                {'id': 'field3.item1', 'title': "Field3_1",
                 'render': UiStdDataGrid.text_render},
                {'id': 'field3.item2', 'title': "Field3_2"},
                {'id': 'field4', 'title': "Other Field 4",
                 'render': UiStdDataGrid.pill_render},
                {'id': 'field5', 'title': "Extra Field 5", 'visible': False,
                 'render': UiStdDataGrid.check_render},
                {'id': 'field6', 'title': "Data Field 6", 'visible': False},
                {'id': 'field7', 'title': "Field Header 7", 'visible': False},
                {'id': 'field8', 'title': "Field8", 'visible': False},
                {'id': 'field9', 'title': "Field Number 9", 'visible': False},
            ],
            'export': {
                'types': ['csv', 'xls', 'print'],
                'file_title': "Example Data",
                'file_prefix': "export",
                'csv_fieldSeparator': ";",
                'csv_fieldBoundary': '',
            },
            'single_ops': [
                {'label': 'Single Operation 1', 'value': "single_op1"},
                {'label': 'Single Op 2 with confirm', 'value': "single_op2",
                 'confirm': 'Are you sure you want to do this operation?'},
            ],
            'group_ops': [
                {'label': 'Group Operation 1', 'value': "group_op1"},
                {'label': 'Group Op 2 with confirm', 'value': "group_op2",
                 'confirm': 'Are you sure?'},
                {'label': 'Op 3 with Reload', 'value': "group_op3"},
            ],
        }
        html = tpl('data_grid.tpl', contents=UiStdDataGrid(options))
        return self.reply(html, doctitle=gettext('Datagrid'))

    def post(self, action='', **kwargs):
        from exonwebui.macros.datagrids import UiStdDataGrid
        if action == 'loaddata':
            data = []
            for k in range(228):
                _k = str(k).rjust(3, '0')
                data.append({
                    'DT_RowId': 'rowid_%s' % _k,
                    'field1': UiStdDataGrid.link(
                        'master_%s' % _k, '#datagrid'),
                    'field2': 'field2 %s' % _k,
                    'field3': {
                        'item1': UiStdDataGrid.text(
                            'field3.1 %s' % _k if randint(0, 2) else ''),
                        'item2': 'field3.2 %s' % _k if randint(0, 3) else '',
                    },
                    'field4': UiStdDataGrid.pill(
                        'Yes' if randint(0, 1) else 'No', 'Yes'),
                    'field5': UiStdDataGrid.check(bool(randint(0, 1))),
                    'field6': 'field6 %s' % _k if randint(0, 1) else '',
                    'field7': 'field7 %s' % _k if randint(0, 1) else '',
                    'field8': 'field8 %s' % _k if randint(0, 1) else '',
                    'field9': 'field9 %s' % _k if randint(0, 1) else '',
                })
            return self.reply(data)

        if action in ['single_op1', 'single_op2',
                      'group_op1', 'group_op2', 'group_op3']:
            rows = request.form.getlist('rows[]')
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


class VLoader(MenuBoardView):
    routes = [('/loader', 'loader')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 2, lazy_gettext('Page Loader'), url='#loader')

    def get(self, **kwargs):
        from exonwebui.macros.basic import UiAlert
        html = UiAlert('message', gettext('loaded after delay'),
                       styles='p-3', dismiss=False)
        html += tpl('progress_loader.tpl')

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
            self.shared_buffer.set('loader_progress', int(i * 100 / t))
            time.sleep(1)

        flash(gettext('success'), 'success')
        return self.reply(None)


class VLoginpage(MenuBoardView):
    routes = [('/loginpage', 'loginpage'),
              ('/loginpage/<action>', 'loginpage_1')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 3, lazy_gettext('Login Page'), url='loginpage')

    def get(self, action='', **kwargs):
        from exonwebui.macros.forms import UiLoginForm

        if action == 'load':
            html = UiLoginForm(
                {'submit_url': url_for('loginpage'), 'authkey': '123456'},
                styles="text-white bg-secondary")
            return self.reply(html, doctitle=gettext('Loginpage'))
        else:
            params = {
                'doc_lang': session.get('lang', ''),
                'doc_langdir': session.get('lang_dir', ''),
                'doc_title': "WebUI",
                'load_url': "%s/load" % url_for('loginpage'),
            }
            return self.reply(tpl('loginpage.tpl', **params))

    def post(self):
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
