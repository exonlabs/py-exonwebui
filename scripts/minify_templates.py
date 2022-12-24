# -*- coding: utf-8 -*-
import os
import sys
from argparse import ArgumentParser


def find_templates(target):
    for root, dirs, files in os.walk(target):
        for fname in files:
            if fname[-3:] == '.j2' and fname[-7:] != '.min.j2':
                src_path = os.path.join(root, fname)
                dst_path = os.path.join(root, "%s.min.j2" % fname[:-3])
                yield (src_path, dst_path)


def minify_tpl(src_path, dst_path, inplace=False):
    # read input
    with open(src_path, 'r') as fsrc:
        src_data = fsrc.readlines()

    # write output
    with open(src_path if inplace else dst_path, 'w+') as fdst:
        for line in src_data:
            fdst.write(line.strip())


def main():
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '--quiet', dest='quiet', action='store_true',
            help="quiet operaton mode")
        pr.add_argument(
            '--inplace', dest='inplace', action='store_true',
            help="minify templates inplace (replace original file)")
        pr.add_argument(
            'target',
            help="target parent folder to search for templates")
        args = pr.parse_args()

        if not (len(args.target) and os.path.exists(args.target)):
            raise ValueError("invalid target path %s" % args.target)

        if not args.quiet:
            print("minify templates under: %s" % args.target)

        for fsrc, fdst in find_templates(args.target):
            if not args.quiet:
                print("template: %s" % fsrc)
            minify_tpl(fsrc, fdst, inplace=args.inplace)

    except Exception as e:
        print("ERROR: %s" % e)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
