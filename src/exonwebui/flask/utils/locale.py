# -*- coding: utf-8 -*-
import os
from flask import current_app, request, session, flash, redirect
import flask_babelex as babelex


# initialize localization with babel extension
def init_locale(app, locale_path=''):
    domain = babelex.Domain(dirname=locale_path)
    babel = babelex.Babel(app, default_domain=domain)

    if locale_path and os.path.exists(locale_path):
        babel.localeselector(lambda: session.get('lang', 'en'))
        app.config['LOCALE_ENABLED'] = True
        app.config['LOCALE_PATH'] = locale_path

        # load available locales
        all_langs = {'en': 'English'}
        for lang in list(os.walk(locale_path))[0][1]:
            fpath = os.path.join(locale_path, lang, 'INFO')
            if os.path.exists(fpath):
                with open(fpath, 'r') as f:
                    all_langs[lang] = f.read().strip()
        if len(all_langs.keys()) > 1:
            app.config['LOCALE_LANGS'] = all_langs

        # register before_request locale operation
        # better to keep this function as first operation to avoid
        # un-necessary operations in case of redirection
        app.before_request(check_locale)

    else:
        app.config['LOCALE_ENABLED'] = False
        app.config['LOCALE_PATH'] = ''
        app.config['LOCALE_LANGS'] = {}


def check_locale():
    if not babelex or not current_app.config.get('LOCALE_ENABLED'):
        return None

    # check session lang
    if not session.get('lang', ''):
        session['lang'] = 'en'
        session['lang_dir'] = 'ltr'

    # check lang change request
    new_lang = request.args.get('lang', '').strip()
    if not new_lang or new_lang == session['lang']:
        return None

    old_lang = session['lang']
    try:
        session['lang'] = new_lang
        if babelex.get_domain().get_translations().info() \
                or new_lang == 'en':
            babelex.refresh()
        else:
            raise Exception(
                "no translation for '%s' lang" % new_lang)
    except Exception as e:
        session['lang'] = old_lang
        flash(str(e).strip(), 'error')

    # adjust lang direction
    if session['lang'] in ['ar', 'fa', 'he', 'ku', 'ur']:
        session['lang_dir'] = 'rtl'
    else:
        session['lang_dir'] = 'ltr'

    return redirect(current_app.config.get('INDEX_URL') or "/")
