# -*- coding: utf-8 -*-
import os
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.webserver import WebServer

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')

cfg = {
    'app': {
        'secret_key': "0123456789ABCDEF",
        'max_content_length': 10485760,
    },
    'engine': {
        'host': '0.0.0.0',
        'port': 8000,
        'workers': 2,
        'max_requests': 200,
        'max_requests_jitter': 50,
    },
}


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', '--debug', action='store_true',
                        help='enable debug mode')
        pr.add_argument('--simple', action='store_true',
                        help='use simple web engine')
        args = pr.parse_args()

        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)

        if args.simple:
            cfg['simple_engine'] = True

        p = WebServer('SampleWebui', options=cfg)
        p.base_path = os.path.dirname(__file__)

        from views import MenuBoardView
        p.views = MenuBoardView.__subclasses__()

        p.start()

    except Exception:
        print(format_exc())
        sys.exit(1)
