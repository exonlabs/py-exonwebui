# -*- coding: utf-8 -*-
import gzip
from io import BytesIO
from flask import current_app, request

__all__ = []


# initialize gzip compression
def init_gzip(app, opts={}):
    app.config['GZIP_OPTS'] = opts

    # register compress response data
    # should be kept as last function, so other after_request functions
    # can access data before compression
    app.after_request(gzip_response)


# gzip response data
def gzip_response(response):
    opts = current_app.config.get('GZIP_OPTS') or {}
    encoding = request.headers.get('Accept-Encoding', '')

    if response.status_code < 200 or \
       response.status_code >= 300 or \
       response.direct_passthrough or \
       len(response.get_data()) < opts.get('minimum_size', 500) or \
       'gzip' not in encoding.lower() or \
       'Content-Encoding' in response.headers:
        return response

    gzip_buffer = BytesIO()
    gzip_file = gzip.GzipFile(
        mode='wb',
        compresslevel=opts.get('compress_level', 6),
        fileobj=gzip_buffer)
    gzip_file.write(response.get_data())
    gzip_file.close()

    response.set_data(gzip_buffer.getvalue())
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = len(response.get_data())

    return response
