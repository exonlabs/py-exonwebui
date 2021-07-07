# -*- coding: utf-8 -*-
import os
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.webapp import BaseWebApp
from views import *  # noqa

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")


if __name__ == '__main__':
    log = logging.getLogger()
    log.name = 'main'
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
            if os.path.exists(link_path):
                os.unlink(link_path)
            src_dir = os.path.join(
                os.path.dirname(base_path), 'exonwebui', n)
            if os.path.exists(src_dir):
                os.symlink(src_dir, link_path)

        cfg = {
            'secret_key': "0123456789ABCDEF",
            'max_content_length': 10485760,
            'templates_auto_reload': bool(args.debug > 0),
        }
        webapp = BaseWebApp(
            'SampleWebui', options=cfg, logger=log, debug=args.debug)
        webapp.base_path = base_path
        webapp.views = MenuBoardView.__subclasses__()
        webapp.initialize()
        webapp.start('0.0.0.0', 8000)

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)
