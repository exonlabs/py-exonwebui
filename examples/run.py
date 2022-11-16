# -*- coding: utf-8 -*-
import os
import sys
import logging
from argparse import ArgumentParser

from exonutils.webapp.server import SimpleWebServer
from exonutils.webapp.extserver import ExtWebServer, WebArbiter

from exonwebui import __file__ as exonwebui_path
from exonwebui.utils.locale import init_locale
from exonwebui.utils.gzip import init_gzip

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


HOST = "0.0.0.0"
PORT = 8000

APP_OPTIONS = {
    'secret_key': "0123456789ABCDEF",
    'max_content_length': 10485760,  # 10MiB
    'templates_auto_reload': False,
}

EXT_OPTIONS = {
    'bind': '%s:%s' % (HOST, PORT),
    'workers': 2,
    'threads': 1,
    'max_requests': 0,
    'timeout': 0,
}


def init_app(websrv, args):
    # disable strict slash matching
    websrv.app.url_map.strict_slashes = False

    # adjust session and csrf cookies attrs
    websrv.app.config['SESSION_COOKIE_HTTPONLY'] = True
    websrv.app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    websrv.app.config['CSRF_COOKIE_HTTPONLY'] = True
    websrv.app.config['CSRF_COOKIE_SAMESITE'] = 'Lax'
    websrv.app.config['CSRF_DISABLE'] = True

    # adjust locale
    locale_path = os.path.join(websrv.base_path, 'locale')
    init_locale(websrv.app, locale_path=locale_path)

    # adjust gzip
    if args.ext_gzip:
        init_gzip(websrv.app)


def main():
    logger = logging.getLogger()
    logger.name = 'main'

    # web requests logger
    reqlog = logging.getLogger('%s.requests' % logger.name)
    reqlog.handlers = [logging.StreamHandler(sys.stdout)]

    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        pr.add_argument(
            '--ext-websrv', dest='ext_websrv', action='store_true',
            help="use extended gunicorn web server")
        pr.add_argument(
            '--ext-gzip', dest='ext_gzip', action='store_true',
            help="use extended gzip compression module")
        args = pr.parse_args()

        if args.debug > 0:
            logger.setLevel(logging.DEBUG)
        if args.debug >= 3:
            APP_OPTIONS['templates_auto_reload'] = True

        # adjust resources links
        base_path = os.path.abspath(os.path.dirname(__file__))
        for n in ['templates', 'static']:
            link_path = os.path.join(base_path, n, 'webui')
            if os.path.isfile(link_path) or os.path.islink(link_path):
                os.unlink(link_path)
            src_dir = os.path.join(
                os.path.dirname(exonwebui_path), n)
            if os.path.exists(src_dir):
                os.symlink(src_dir, link_path)

        websrv = SimpleWebServer(
            name='WebUiPortal', options=APP_OPTIONS,
            logger=logger, reqlogger=reqlog)
        websrv.base_path = base_path
        websrv.initialize()

        init_app(websrv, args)

        from views import MenuBoardView
        for view_cls in MenuBoardView.__subclasses__():
            websrv.add_view(view_cls())

        if args.ext_websrv:
            ext_websrv = ExtWebServer(websrv, options=EXT_OPTIONS)
            WebArbiter(ext_websrv).run()
        else:
            websrv.start(
                HOST, PORT,
                debug=bool(args.debug >= 1),
                use_reloader=bool(args.debug >= 3))

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)


if __name__ == '__main__':
    main()
