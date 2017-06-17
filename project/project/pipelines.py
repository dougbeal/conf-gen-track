# -*- coding: utf-8 -*-
import re

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
    
import scrapy
import project.spiders.spin as spin

from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.media import MediaPipeline
from scrapy.exporters import JsonItemExporter
from scrapy.exceptions import DropItem

# functions used in MediaPipeline.process_item override
from twisted.internet.defer import Deferred, DeferredList

from scrapy.utils.misc import md5sum
from scrapy.utils.misc import arg_to_iter

from slugify import slugify
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JsonPipeline(object):
  def __init__(self):
    self.file = open("spin.json", 'wb')
    self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
    self.exporter.start_exporting()
 
  def close_spider(self, spider):
    self.exporter.finish_exporting()
    self.file.close()
 
  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item    

def addRaw( url ):
    return re.sub(r"^(.*)/([^/]+)$",
                  r"\1/raw/\2",
                  url)
  
class PastebinPipeline(FilesPipeline):

  class SpiderInfoItem(MediaPipeline.SpiderInfo):
    def __init__(self, spider, item):
      self.item = item
      super(PastebinPipeline.SpiderInfoItem, self).__init__(spider)
    
  def __init__(self, store_uri, download_func=None, settings=None):
    cls_name = "PastebinPipeline"
    print cls_name
    m_store_uri = settings['M_STORE']
    self.m_store = self._get_store(m_store_uri)
    super(PastebinPipeline, self).__init__(store_uri=store_uri, download_func=download_func, settings=settings)
    
  def get_media_requests(self, item, info):
    if 'file_urls' in item:
      for file_url in item['file_urls']:
        url = file_url
        if not 'raw' in file_url:
          url = addRaw(file_url)
        yield scrapy.Request(url)

  # override MediaPipeline.process_item so the item is in the info so
  # file_downloaded can use item to create filename
  def process_item(self, item, spider):
    print "process_item"
    info = self.SpiderInfoItem(spider, item)
    requests = arg_to_iter(self.get_media_requests(item, info))
    dlist = [self._process_request(r, info) for r in requests]
    dfd = DeferredList(dlist, consumeErrors=1)
    return dfd.addCallback(self.item_completed, item, info)
  
  def file_downloaded(self, response, request, info):
    path = self.file_path(request, response=response, info=info)
    buf = BytesIO(response.body)
    checksum = md5sum(buf)

    buf.seek(0)
    self.store.persist_file(path, buf, info)

    item = info.item
    filename = u' '.join((item['emulator_name'], item['name']))
    path = os.path.join(map(slugify, [ item['resolution'], filename ]))
    
    buf.seek(0)
    print "file_downloaded: " + path
    self.m_store.persist_file( os.path.join(path, name), buf, info)
                               
    return checksum
