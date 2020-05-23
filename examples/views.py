# -*- coding: utf-8 -*-
import os
import time
from flask import session, flash, request, url_for, render_template as tpl
from flask_babelex import gettext, lazy_gettext

from exonwebui.menuboard import MenuBoardView
from exonwebui.macros import Macro


class VIndex(MenuBoardView):
    routes = [('/', 'index')]

    @classmethod
    def initialize(cls, websrv, app):
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
        cls.add_menulink(app, 1, lazy_gettext('UI Components'))

    def get(self, **kwargs):
        params = {
            'page_lang': session.get('lang', ''),
            'page_langdir': session.get('lang_dir', ''),
            'page_doctitle': "WebUI",
        }

        if not session.get('simpleboard', None):
            session['simpleboard'] = False
        if request.args.get('toogleboard', '').strip():
            session['simpleboard'] = not session['simpleboard']
            return self.redirect(url_for('index'))

        if session.get('simpleboard', False):
            return tpl('simpleboard.tpl', **params)
        else:
            return tpl('mainboard.tpl', **params)


class VHome(MenuBoardView):
    routes = [('/home', 'home')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(app, 0, lazy_gettext('Home'), url='#home')

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
        flash(gettext('error'), 'error')
        flash(gettext('warning'), 'warn')
        flash(gettext('info'), 'info')
        flash(gettext('success'), 'success')
        html = Macro.alert(
            'message', gettext('showing notifications'), styles='p-3')
        return self.reply(html, doctitle=gettext('Notifications'))


class VAlerts(MenuBoardView):
    routes = [('/alerts', 'alerts')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 2, lazy_gettext('Alerts'), url='#alerts', parent=1)

    def get(self, **kwargs):
        html = Macro.alert(
            'info', gettext('info'), styles='px-3 pt-3', dismissible=True)
        html += Macro.alert(
            'warn', gettext('warning'), styles='px-3', dismissible=True)
        html += Macro.alert(
            'error', gettext('error'), styles='px-3', dismissible=True)
        html += Macro.alert(
            'success', gettext('success'), styles='px-3', dismissible=True)
        html += Macro.alert(
            'message', gettext('message'), styles='px-3', dismissible=True)
        return self.reply(html, doctitle=gettext('Alerts'))


class VLoader(MenuBoardView):
    routes = [('/loader', 'loader')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 2, lazy_gettext('Page Loader'), url='#loader')

    def get(self, **kwargs):
        html = Macro.alert(
            'message', gettext('loaded after delay'), styles='p-3')
        html += tpl('progress_loader.tpl')

        # simulate delay
        time.sleep(5)

        return self.reply(html, doctitle=gettext('Page Loader'))

    def post(self, **kwargs):
        # get loading progress status
        if request.form.get('get_progress', ''):
            res = self.shared_buffer.get('loader_progress', 0)
            return self.reply(res)

        # simulate long delay
        t = 20
        for i in range(t):
            self.shared_buffer.set('loader_progress', int(i * 100 / t))
            time.sleep(1)

        flash(gettext('success'), 'success')
        return self.reply(None)


class VLoginpage(MenuBoardView):
    routes = [('/loginpage', 'loginpage')]

    @classmethod
    def initialize(cls, websrv, app):
        cls.add_menulink(
            app, 3, lazy_gettext('Login Page'), url='loginpage')

    def get(self, **kwargs):
        params = {
            'page_lang': session.get('lang', ''),
            'page_langdir': session.get('lang_dir', ''),
            'page_doctitle': "Login | WebUI",
            'loginform': Macro.loginform(
                url_for('loginpage'), '123456',
                styles="text-white bg-secondary"),
        }
        return tpl('loginpage.tpl', **params)

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

        flash(err, 'error')
        return self.reply(None)
