#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Clean certain ext files
"""
import os


class Cleaner(object):
    """Cleaner class
    """
    def __init__(self, path, ext):
        self._path = path
        self._ext = ext

    def run(self):
        print 'Scanning all deep down ' + os.path.abspath(self._path) + '...'
        counter = 0
        for (path, dirs, files) in os.walk(self._path):
            counters = 0
            for filename in files:
                if filename.endswith(self._ext):
                    try:
                        os.remove(os.path.join(path, filename))
                        counter += 1
                        counters += 1
                    except:
                        print os.path.join(path, filename) + ' remove failed'
            if counters > 0:
                print str(counters) + (' files are removed' if counters > 1 \
                                else ' file is removed') + ' inside ' + path
        print str(counter) + (' files are removed' if counter > 1 \
                                else ' file is removed')


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-p", "--path", dest="path", help="The root path...")
    parser.add_option("-e", "--ext", dest="ext", help="The file extensions that you want to delete...")

    (options, args) = parser.parse_args()

    path, ext = options.path, options.ext
    if path and ext:
        Cleaner(path, ext).run()
    else:
        print "必须提供根目录和要删除文件的后缀名... （使用-h获取帮助）"
