# -*- coding: utf-8 -*-
import os
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

import exonwebui
from exonutils.webapp import BaseWebSrv
from views import MenuBoardView

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


if __name__ == '__main__':
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
            logging.getLogger().setLevel(logging.DEBUG)

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

        cfg = {
            'secret_key': "0123456789ABCDEF",
            'max_content_length': 10485760,
            'templates_auto_reload': bool(args.debug > 0),
        }

        webapp = BaseWebSrv(
            'SampleWebui', options=cfg, logger=logger, debug=args.debug)
        webapp.base_path = base_path
        webapp.initialize()
        webapp.load_views(MenuBoardView.__subclasses__())
        webapp.start('0.0.0.0', 8000)

    except Exception:
        logger.fatal(format_exc())
        sys.exit(1)
