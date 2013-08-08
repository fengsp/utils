#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Just a simple img downloader of web page right now...
"""
import urllib, threading, Queue, re, os

from utils import gamble

NUM_WORKERS = 15
q = Queue.Queue(0)
FILENAMES = []
FILENAMES_LOCK = threading.Lock()


class DownloadWorker(threading.Thread):
    """Worker of multithreading
    """
    __slots__ = []

    def __init__(self, path):
        self._path = path
        self._queue = q
        super(DownloadWorker, self).__init__()

    def run(self):
        while True:
            try:
                download_url = self._queue.get()
                if download_url is not None:
                    self._download(download_url)
                    self._queue.task_done()
            except:
                continue

    def _get_path(self, url):
        filename = url.split('/')[-1]
        if not filename:
            filename = url.split('/')[-2]
        if not filename.endswith('.jpg'):
            filename += '.jpg'
        FILENAMES_LOCK.acquire()
        while filename in FILENAMES:
            rindex = filename.rindex('.')
            filename = filename[0:rindex] + gamble() + filename[rindex:]
        FILENAMES.append(filename)
        FILENAMES_LOCK.release()
        return os.path.join(self._path, filename)
    
    def _download(self, url):
        path = self._get_path(url)
        try:
            urllib.urlretrieve(url, path)
        except:
            print "Downloading " + url + " failed..."
        

class Downloader(object):
    """Core class
    """
    def __init__(self, url, path):
        self._queue = q
        self._url = url
        self._img_src = re.compile(r'<img.*?src="(?P<url>.*?)".*?>', re.I|re.S)
        self._path = path
        self.initialize()

    def initialize(self):
        counter = 0
        for filename in os.listdir(path):
            FILENAMES.append(filename)
        urls = self._parse_url()
        urls = set(urls)
        for url in urls:
            counter += 1
            self._queue.put(url)
        print "获取到" + str(counter) + "个图片链接"

    def _parse_url(self):
        try:
            html_content = urllib.urlopen(self._url).read()
        except:
            print "获取html内容失败...."
            raise SystemExit
        for img in self._img_src.finditer(html_content):
            yield img.group('url')
    
    def run(self):
        for i in range(NUM_WORKERS):
            worker = DownloadWorker(self._path)
            worker.setDaemon(True)
            worker.start()
        self._queue.join()


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-u", "--url", dest="url", help="The destination of your content")
    parser.add_option("-p", "--path", dest="path", help="The destination location")
    (options, args) = parser.parse_args()

    url = options.url if options.url else None
    path = options.path if options.path else None
    if url and path:
        Downloader(url, path).run()
    else:
        print "必须提供目标URI和本地存储路径... （使用-h获取帮助)"
