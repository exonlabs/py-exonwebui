# -*- coding: utf-8 -*-
import os
import gzip
from io import BytesIO
from flask import current_app, request, session, redirect, \
    jsonify, flash, get_flashed_messages
from flask_babelex import Babel, Domain, get_domain, refresh

from exonutils._backport.v5.webapp import BaseWebView

from exonwebui.macros.basic import UiAlert

__all__ = []


class MenuBoardView(BaseWebView):

    # index page url
    index_url = '/'

    # enable minimize output html response data
    mindata_enable = True

    # enable gzip response data
    gzip_enable = True
    gzip_compress_level = 6
    gzip_minimum_size = 500

    @classmethod
    def board_initialize(cls, app, locale_path=''):
        if not app.config.get('MENUBOARD_INIT', False):
            # initialize gzip
            if cls.gzip_enable:
                app.after_request(cls.gzip_response)

            # initialize localization with babel extension
            domain = Domain(dirname=locale_path)
            babel = Babel(app, default_domain=domain)
            babel.localeselector(lambda: session.get('lang', 'en'))
            app.config['LOCALE_ENABLED'] = bool(
                locale_path and os.path.exists(locale_path))
            app.config['LOCALE_PATH'] = locale_path

            # set jinja global variables
            app.jinja_env.globals['get_menulinks'] = cls.get_menulinks

            # set board init flag
            app.config['MENUBOARD_INIT'] = True

    # board menu methods ###############

    @classmethod
    def get_menulinks(cls, app=None):
        if not app:
            app = current_app

        return cls.format_menulinks(
            app.config.get('MENUBOARD_MENUBUFFER', []))

    @classmethod
    def format_menulinks(cls, buffer):
        # BOARD_SIDEMENU dict structure:
        # {0: {'label': ..., 'icon': ..., 'url': ...},
        #  1: {'label': ..., 'icon': ..., 'url': '#',
        #      'menu': {0: {'label': ..., 'icon': ..., 'url': ...},
        #               1: {'label': ..., 'icon': ..., 'url': ...}}},
        # }
        menu = {}

        for index, label, icon, url, parent in buffer:
            # standalone link
            if parent is None:
                if index in menu:
                    menu[index].update({
                        'label': label, 'icon': icon, 'url': url})
                else:
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

        return menu

    @classmethod
    def add_menulink(cls, app, index, label, icon=None, url='#',
                     parent=None):
        # index:  number/order of link in menu or submenu
        # label:  link label to show
        # icon:   icon to show for links or headers
        # url:    url for active links and '#' for submenu headers
        # parent: index of parent menu for submenu links
        buff = app.config.get('MENUBOARD_MENUBUFFER', [])
        buff.append([index, label, icon, url, parent])
        app.config['MENUBOARD_MENUBUFFER'] = buff

    # gzip response data
    @classmethod
    def gzip_response(cls, response):
        accept_encoding = request.headers.get('Accept-Encoding', '')

        if response.status_code < 200 or \
           response.status_code >= 300 or \
           response.direct_passthrough or \
           len(response.get_data()) < cls.gzip_minimum_size or \
           'gzip' not in accept_encoding.lower() or \
           'Content-Encoding' in response.headers:
            return response

        gzip_buffer = BytesIO()
        gzip_file = gzip.GzipFile(
            mode='wb',
            compresslevel=cls.gzip_compress_level,
            fileobj=gzip_buffer)
        gzip_file.write(response.get_data())
        gzip_file.close()
        response.set_data(gzip_buffer.getvalue())
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(response.get_data())

        return response

    # xhr request validation
    @classmethod
    def request_xhr(cls):
        if 'X-Requested-With' in request.headers and \
           request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return True
        return False

    # minimize data by removing line breaks and extra white spaces
    @classmethod
    def minimize_data(cls, data):
        if type(data) is str:
            return ''.join([l.strip() for l in data.split('\n')])
        return data

    # redirect methods ###############

    @classmethod
    def redirect(cls, url, blank=False):
        if cls.request_xhr():
            return jsonify(redirect=url, blank=blank)
        return redirect(url)

    # reply methods ###############

    @classmethod
    def reply(cls, response, **params):
        if cls.mindata_enable:
            response = cls.minimize_data(response)
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
        else:
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

    # request handling ###############

    @classmethod
    def before_request(cls):
        # locale handling
        if current_app.config.get('LOCALE_ENABLED', False):
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
                        if get_domain().get_translations().info() \
                           or new_lang == 'en':
                            refresh()
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

                return cls.redirect(cls.index_url)

        return None
