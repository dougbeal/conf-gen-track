import scrapy
from scrapy.loader import ItemLoader
from project.items import ScriptItem
from project.items import TabItem
from project.items import EmulatorItem

from pprint import pprint as pp

DIR_TO_EM = {
  'm': 'memu-installation.html'
}

EM_TO_DIR = {value: key for key, value in DIR_TO_EM.iteritems()}

DIR_TO_R = {
  'a': '1080x1920',
  'd': '800x1280',
  'g': '720x1280',
  'j': '480x854'
  }

R_TO_DIR = {value: key for key, value in DIR_TO_R.iteritems()}

TAB_PREFIX = "content"

def merge_text_list( text_list):
  return unicode.strip( u''.join(text_list) )

class Spin(scrapy.Spider):
  name = 'spin'

  start_urls = ['http://www.ffbemacro.com/memu-installation.html']

  def parse(self, response):
    emulator_item = ItemLoader(item = EmulatorItem(), response = response)
    #substring('FLAC',1,4*contains(//tr/td[@class='left']/following-sibling::text()[1], 'FLAC'))

    emulator_item.add_xpath("name", "substring-after(//title/text(), ' - ')")

    tabs = response.selector.xpath('.//span[starts-with(@name, "%s")]' % TAB_PREFIX)
    #tabs_name = map(unicode.strip, tabs.xpath('@name').extract())
    #pp(tabs_name)

    emulator_item.add_value( 'tabs', self.extractTabs(tabs) )
    emulator = emulator_item.load_item()
    yield emulator
    for tab in emulator['tabs']:
      yield tab
      for script in tab['scripts']:
        script['emulator_name'] = emulator['name']
        yield script

  def extractTabs(self, selector):
    tabs = []
    for tab in selector:
      tab_item = ItemLoader(item = TabItem(), selector = tab)

      tab_name = tab.xpath('./@name').extract_first()
      tab_index = int(tab_name.replace( TAB_PREFIX, '', 1)) - 1

      #pp(u"tab_name: %s index %i" % (tab_name, tab_index))

      tab_item.tab_index = tab_index

      tab_item.add_value("scripts", self.extractScript(tab))
      tabs.append(dict(tab_item.load_item()))
    return tabs


  def extractScript(self, selector):
    scripts = []
    tab_table = selector.xpath('.//table/tbody')

    resolution_path = './/table/tbody//tr//th//br/following-sibling::text()'
    #print selector.xpath(resolution_path).extract_first()

    #  name,                refil,        pastebin_url,     duration,  settings
    # [u'Version 480x854', u'Refills?', u'Pastebin Link', u'Runtime', u'Settings']
    for row_node in tab_table.xpath('.//tr'):

      script_item = ItemLoader(item = ScriptItem(), selector = row_node)

      # comes from header
      script_item.add_value('resolution', selector.xpath(resolution_path).extract_first())

      value_template = '(.//td)[%i]//text()'
      href_template = '(.//td)[%i]//a/@href'      
      child_number = 1
      script_item.add_xpath('name', value_template % child_number)

      child_number = 1 + child_number
      script_item.add_xpath('refill', value_template % child_number)

      child_number = 1 + child_number     
      script_item.add_xpath('pastebin_url', href_template % child_number)
      script_item.add_xpath('file_urls', href_template % child_number)      

      child_number = 1 + child_number     
      script_item.add_xpath('duration', value_template % child_number)
      
      child_number = 1 + child_number
      #print row_node.xpath('(.//td)[%i]' % child_number ).extract()
      script_item.add_xpath('setting_note', value_template % child_number)
      script_item.add_xpath('setting_image_url', href_template % child_number)
      script_item.add_xpath('image_urls', href_template % child_number)
      
      scripts.append(dict(script_item.load_item()))
    return scripts
