# -*- coding: utf-8 -*-
import os
import sys


def minify_tpl(src_path, dst_path):
    with open(dst_path, 'w+') as fdst:
        with open(src_path, 'r') as fsrc:
            for line in fsrc.readlines():
                fdst.write(line.strip())


def find_templates(target):
    for root, dirs, files in os.walk(target):
        for fname in files:
            if fname[-3:] == '.j2' and fname[-7:] != '.min.j2':
                src_path = os.path.join(root, fname)
                dst_path = os.path.join(root, "%s.min.j2" % fname[:-3])
                yield (src_path, dst_path)


def main():
    try:
        if not (len(sys.argv) >= 2 and sys.argv[1]):
            raise ValueError("please specify target path")

        target = sys.argv[1]
        if not os.path.exists(target):
            raise ValueError("invalid target path %s" % target)

        for fsrc, fdst in find_templates(target):
            minify_tpl(fsrc, fdst)

    except Exception as e:
        print(e)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
