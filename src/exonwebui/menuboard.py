# -*- coding: utf-8 -*-
import os
from flask import current_app, request, session, redirect, \
    jsonify, flash, get_flashed_messages
try:
    import flask_babelex as babelext
except ImportError:
    babelext = None

from exonutils.webapp.view import BaseWebView

from .macros.basic import UiAlert

__all__ = []


class MenuBoardView(BaseWebView):

    # index page url
    index_url = '/'

    @classmethod
    def board_initialize(cls, app, locale_path=''):
        # initialize localization with babel extension
        if babelext:
            domain = babelext.Domain(dirname=locale_path)
            babel = babelext.Babel(app, default_domain=domain)
            babel.localeselector(lambda: session.get('lang', 'en'))
            app.config['LOCALE_ENABLED'] = bool(
                locale_path and os.path.exists(locale_path))
        else:
            app.config['LOCALE_ENABLED'] = False
        app.config['LOCALE_PATH'] = locale_path

        # set jinja global variables
        app.jinja_env.globals['get_menulinks'] = cls.get_menulinks

    @classmethod
    def get_menulinks(cls, app=None):
        if not app:
            app = current_app

        return app.config.get('MENUBOARD_MENUBUFFER') or {}

    @classmethod
    def add_menulink(cls, app, index, label, icon=None, url='#', parent=None):
        # index:  number/order of link in menu or submenu
        # label:  link label to show
        # icon:   icon to show for links or headers
        # url:    url for active links and '#' for submenu headers
        # parent: index of parent menu for submenu links

        # menu dict structure:
        # {0: {'label': ..., 'icon': ..., 'url': ...},
        #  1: {'label': ..., 'icon': ..., 'url': '#',
        #      'menu': {0: {'label': ..., 'icon': ..., 'url': ...},
        #               1: {'label': ..., 'icon': ..., 'url': ...}}},
        # }
        menu = app.config.get('MENUBOARD_MENUBUFFER') or {}

        # standalone link
        if parent is None:
            menu.update({
                index: {'label': label, 'icon': icon, 'url': url}})
        # submenu link
        else:
            if parent not in menu:
                menu[parent] = {'menu': {}}
            elif 'menu' not in menu[parent]:
                menu[parent]['menu'] = {}
            menu[parent]['menu'].update(
                {index: {'label': label, 'icon': icon, 'url': url}})

        app.config['MENUBOARD_MENUBUFFER'] = menu

    # xhr request validation
    @classmethod
    def request_xhr(cls):
        if 'X-Requested-With' in request.headers and \
           request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return True
        return False

    @classmethod
    def redirect(cls, url, blank=False):
        if cls.request_xhr():
            return jsonify(redirect=url, blank=blank)
        return redirect(url)

    @classmethod
    def reply(cls, response, **params):
        if cls.request_xhr():
            if response is not None:
                params['payload'] = response

            notifications = get_flashed_messages(with_categories=True)
            if notifications:
                params['notifications'] = []
                for cat, msg in notifications:
                    if '.' in cat:
                        _cat, opts = cat.split('.', 1)
                        params['notifications'].append(
                            [_cat, msg, 'u' in opts, 's' in opts])
                    else:
                        params['notifications'].append(
                            [cat, msg, False, False])

            return jsonify(**params)

        return response if response is not None else ''

    @classmethod
    def alert(cls, message, category='error', **params):
        response = UiAlert(category, message)
        return cls.reply(response, **params)

    @classmethod
    def notify(cls, message, category='error', unique=False,
               sticky=False, **params):
        opts = 'u' if unique else ''
        opts += 's' if sticky else ''
        flash(message, '%s.%s' % (category, opts) if opts else category)
        return cls.reply(None, **params)

    def before_request(self, *args, **kwargs):
        # locale handling
        if babelext and current_app.config.get('LOCALE_ENABLED'):
            # check session lang
            if not session.get('lang', ''):
                session['lang'] = 'en'
                session['lang_dir'] = 'ltr'

            # check lang change request
            new_lang = request.args.get('lang', '').strip()
            if new_lang:
                if new_lang != session['lang']:
                    old_lang = session['lang']
                    try:
                        session['lang'] = new_lang
                        if babelext.get_domain().get_translations().info() \
                                or new_lang == 'en':
                            babelext.refresh()
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

                return self.redirect(self.index_url)

        return None
