# -*- coding: utf-8 -*-
import gzip
from io import BytesIO
from flask import request

from .menuboard import MenuBoardView

__all__ = []


class ExtMenuBoardView(MenuBoardView):

    # enable minimize output html response data
    mindata_enable = True

    # enable gzip response data
    gzip_enable = True
    gzip_compress_level = 6
    gzip_minimum_size = 500

    @classmethod
    def board_initialize(cls, app, **kwargs):
        if cls.gzip_enable:
            app.after_request(cls.gzip_response)

        super(ExtMenuBoardView, cls).board_initialize(app, **kwargs)

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

    # minimize data by removing line breaks and extra white spaces
    @classmethod
    def minimize_data(cls, data):
        if type(data) is str:
            return ''.join([l.strip() for l in data.split('\n')])
        return data

    @classmethod
    def reply(cls, response, **params):
        if response and cls.mindata_enable:
            response = cls.minimize_data(response)

        return super(ExtMenuBoardView, cls).reply(response, **params)
