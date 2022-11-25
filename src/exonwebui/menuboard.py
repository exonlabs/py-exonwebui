# -*- coding: utf-8 -*-
from flask import redirect, jsonify, flash, get_flashed_messages
from exonutils.webapp.view import BaseWebView

from .macros.basic import UiAlert

__all__ = []


class MenuBoardView(BaseWebView):

    # menu structure:
    # {0: {'label': ..., 'icon': ..., 'url': ...},
    #  1: {'label': ..., 'icon': ..., 'url': '#',
    #      'submenu': {0: {'label': ..., 'icon': ..., 'url': ...},
    #                  1: {'label': ..., 'icon': ..., 'url': ...}}},
    # }
    @classmethod
    def add_menulink(cls, menu_buffer, index, label, icon=None,
                     url='#', parent=None):
        # menu_buffer:   current menu dict buffer to append to
        # index:  number/order of link in menu or submenu
        # label:  link label to show
        # icon:   icon to show for links or headers
        # url:    url for active links and '#' for submenu headers
        # parent: index of parent menu for submenu links

        # standalone link
        if parent is None:
            menu_buffer.update({
                index: {'label': label, 'icon': icon, 'url': url}})

        # submenu link
        else:
            if parent not in menu_buffer:
                menu_buffer[parent] = {'submenu': {}}
            elif 'submenu' not in menu_buffer[parent]:
                menu_buffer[parent]['submenu'] = {}
            menu_buffer[parent]['submenu'].update(
                {index: {'label': label, 'icon': icon, 'url': url}})

        return menu_buffer

    @classmethod
    def redirect(cls, url, blank=False, dyn_jsonify=True):
        if dyn_jsonify and not cls.is_jsrequest():
            return redirect(url)

        return jsonify(redirect=url, blank=blank)

    @classmethod
    def reply(cls, response, dyn_jsonify=True, **params):
        if dyn_jsonify and not cls.is_jsrequest():
            return response

        if response is not None:
            params['payload'] = response

        notifications = get_flashed_messages(with_categories=True)
        if notifications:
            if type(params.get('notifications')) is not list:
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
