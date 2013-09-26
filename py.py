#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Used to generate one py file
"""
import os


def generate(filepath):
    filepath = os.path.abspath(filepath)
    f = open(filepath, 'w')
    f.write(
'''#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
"""''')
    f.close()


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-p", "--path", dest="path", help="The file path...")

    (options, args) = parser.parse_args()
    path = options.path
    if path:
        generate(path)
    else:
        print "必须提供文件路径...  (使用-h获取帮助)"
