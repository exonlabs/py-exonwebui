# -*- coding: utf-8 -*-
import os
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.webapp import BaseWebApp
from views import *  # noqa

try:
    import colorama
    colorama.init()
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

rlog = logging.getLogger('werkzeug')
rlog.setLevel(logging.INFO)
rlog.propagate = False


if __name__ == '__main__':
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='count', default=0,
                        help='set debug modes')
        args = pr.parse_args()

        if args.debug > 0:
            logging.getLogger().setLevel(logging.DEBUG)

        cfg = {
            'secret_key': "0123456789ABCDEF",
            'max_content_length': 10485760,
            'templates_auto_reload': bool(args.debug > 0),
        }
        webapp = BaseWebApp('SampleWebui', options=cfg)
        webapp.base_path = os.path.dirname(__file__)
        webapp.views = MenuBoardView.__subclasses__()
        webapp.create_app().run(
            host='0.0.0.0',
            port='8000',
            debug=bool(args.debug >= 1),
            use_reloader=bool(args.debug >= 3))

    except Exception:
        log.fatal(format_exc())
        sys.exit(1)
