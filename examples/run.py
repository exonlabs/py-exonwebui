# -*- coding: utf-8 -*-
import os
import sys
import logging
from argparse import ArgumentParser

import exonwebui
from exonutils.webapp.server import SimpleWebServer

from views import MenuBoardView

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
                os.path.dirname(exonwebui.__file__), n)
            if os.path.exists(src_dir):
                os.symlink(src_dir, link_path)

        websrv = SimpleWebServer(
            name='WebUiPortal', options=APP_OPTIONS,
            logger=logger, reqlogger=reqlog)
        websrv.base_path = base_path
        websrv.initialize()

        for view_cls in MenuBoardView.__subclasses__():
            websrv.add_view(view_cls())

        websrv.start(
            HOST, PORT,
            debug=bool(args.debug >= 1),
            use_reloader=bool(args.debug >= 3))

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)


if __name__ == '__main__':
    main()
