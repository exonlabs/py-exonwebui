# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from flask import current_app, request, session, redirect, jsonify, url_for
from flask import flash, get_flashed_messages
from flask_seasurf import SeaSurf
from flask_babelex import Babel, Domain, get_domain, refresh as lang_refresh

from exonutils.webserver import WebView
from .macros import Macro


class MenuBoardView(WebView):

    @classmethod
    def board_initialize(cls, app, locale_path=''):
        if not app.config.get('MENUBOARD_INIT', False):
            # initialize seasurf extension
            SeaSurf(app)

            # initialize babel extension
            domain = Domain(dirname=locale_path)
            babel = Babel(app, default_domain=domain)
            if locale_path and os.path.isdir(locale_path):
                babel.localeselector(lambda: session.get('lang', 'en'))
                app.config['LOCALE_ENABLED'] = True
                app.config['LOCALE_PATH'] = locale_path
            else:
                app.config['LOCALE_ENABLED'] = False
                app.config['LOCALE_PATH'] = ''

            # set jinja global varuables
            app.jinja_env.globals['get_menulinks'] = cls.get_menulinks

            # set board init flag
            app.config['MENUBOARD_INIT'] = True

    # board menu methods ###############

    @classmethod
    def get_menulinks(cls, app=None):
        # BOARD_SIDEMENU dict structure:
        # {0: {'label': ..., 'url': ...},
        #  1: {'label': ..., 'url': '#',
        #      'menu': {0: {'label': ..., 'url': ...},
        #               1: {'label': ..., 'url': ...}}},
        # }
        if not app:
            app = current_app
        return app.config.get('MENUBOARD_MENULINKS', {})

    @classmethod
    def add_menulink(cls, app, index, label, url='#', parent=None):
        menu = app.config.get('MENUBOARD_MENULINKS', {})
        if parent is not None:
            if parent not in menu:
                menu[parent] = {'menu': {}}
            elif 'menu' not in menu[parent]:
                menu[parent]['menu'] = {}
            menu[parent]['menu'].update(
                {index: {'label': label, 'url': url}})
        else:
            if index not in menu:
                menu.update({index: {'label': label, 'url': url}})
            else:
                menu[index].update({'label': label, 'url': url})
        app.config['MENUBOARD_MENULINKS'] = menu

    # xhr request validation
    def request_xhr(self):
        if 'X-Requested-With' in request.headers and \
           request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return True
        return False

    # redirect methods ###############

    def redirect(self, url, blank=False):
        if self.request_xhr():
            return jsonify(redirect=url, blank=blank)
        else:
            return redirect(url)

    # reply methods ###############

    def reply(self, response, **params):
        if self.request_xhr():
            if response is not None:
                params['payload'] = response
            notifications = get_flashed_messages(with_categories=True)
            if notifications:
                params['notifications'] = notifications
            return jsonify(**params)
        else:
            return response if response is not None else ''

    def alert(self, message, category='error', **params):
        response = Macro.alert(category, message)
        return self.reply(response, **params)

    def notify(self, message, category='error', **params):
        flash(message, category)
        return self.reply(None, **params)

    # request handling ###############

    def _before_request(self):
        # locale handling
        if current_app.config.get('LOCALE_ENABLED', False):
            # check session lang
            if not session.get('lang', ''):
                session['lang'] = 'en'
                session['lang_dir'] = 'ltr'

            # check lang change request
            new_lang = request.args.get('lang', '').strip()
            if new_lang and new_lang != session['lang']:
                old_lang = session['lang']
                try:
                    session['lang'] = new_lang
                    if get_domain().get_translations().info() \
                       or new_lang == 'en':
                        lang_refresh()
                    else:
                        raise Exception(
                            "no [%s] translation available" % new_lang)
                except Exception as e:
                    session['lang'] = old_lang
                    flash(str(e).strip(), 'error')

                # adjust lang direction
                if session['lang'] in ['ar', 'fa', 'he', 'ku', 'ur']:
                    session['lang_dir'] = 'rtl'
                else:
                    session['lang_dir'] = 'ltr'

                if request.endpoint:
                    return self.redirect(url_for(request.endpoint))
                else:
                    return self.redirect(url_for('index'))

        return self.before_request()

    def _after_request(self, response):
        return self.after_request(response)
