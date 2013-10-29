#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    imgresizer
    ~~~~~~~~~~

    A Image Resizer
    After multiple tests, multi-threading works best.

    :copyright: (c) 2013 by fsp.
    :license: BSD.
"""

import sys
import os
import Queue
from multiprocessing import cpu_count
from threading import Thread, Lock

from PIL import Image


NUM_WORKERS = cpu_count()
size_queue = Queue.Queue(0)


class ImgResizer(object):
    """Main Class
    """
    def __init__(self, filepath, dest_dir=None):
        if dest_dir is None:
            dest_dir = os.path.dirname(filepath)
        self.dest_dir = os.path.abspath(dest_dir)

        basename = os.path.basename(filepath)
        filename, ext = os.path.splitext(basename)
        self.filename = filename
        self.ext = ext

        self.im = Image.open(filepath)

    def resize(self, width, height):
        im = self.im.copy()
        im.thumbnail((width, height), Image.ANTIALIAS)
        resized_filename = self.filename + '_' + str(width) + '_' \
            + str(height) + self.ext
        im.save(os.path.join(self.dest_dir, resized_filename))


class ImgResizeWorker(Thread):
    """Worker used for image resize
    """
    __slots__ = []

    def __init__(self, resizer):
        self._resizer = resizer
        self._queue = size_queue
        super(ImgResizeWorker, self).__init__()

    def run(self):
        while True:
            width, height = self._queue.get()
            self._resizer.resize(width, height)
            self._queue.task_done()


def thumbnail(src_file, dest_dir, max_width):
    """The glue for ImgResizer and ImgResizeWorker

    :param src_file: The src image path
    :param dest_dir: The destination location for ouput,
                     Default to be src image dir
    :param max_width: The max width for your thumbnails
                      Generating output range from 0 to max_width
    """
    width = int(max_width) if max_width else 512
    height = width
    while width > 0:
        size_queue.put((width, height))
        width -= 1
        height -= 1

    for i in range(NUM_WORKERS):
        resizer = ImgResizer(src_file, dest_dir)
        worker = ImgResizeWorker(resizer)
        worker.setDaemon(True)
        worker.start()
    size_queue.join()


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--dest", dest="dest_dir", help="destination directory for images storing")
    parser.add_option("-s", "--src", dest="src_file", help="source image filepath")
    parser.add_option("-m", "--maxwidth", dest="max_width", help="output image maxwidth")
    (options, args) = parser.parse_args()
    
    src_file = getattr(options, 'src_file')
    if src_file is None:
        print '必须提供源图片文件(使用-h获取帮助)'
        sys.exit(0)
    dest_dir = getattr(options, 'dest_dir')
    max_width = getattr(options, 'max_width')

    thumbnail(src_file, dest_dir, max_width)
