import scrapy
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

def merge_text_list( text_list):
  return unicode.strip( u''.join(text_list) )
  
class Spin(scrapy.Spider):
  name = 'spin'
  start_urls = ['http://www.ffbemacro.com/memu-installation.html']

  def parse(self, response):
    resolutions = response.selector.xpath('//li[starts-with(@name, "tab")]')
    print "Resolutions"
    resolution_tabs = resolutions.xpath('@name').extract()
    resolutions = map(unicode.strip, resolutions.xpath('div/text()').extract())
    pp(resolution_tabs)
    pp(resolutions)    
    
    tabs = response.selector.xpath('.//span[starts-with(@name, "content")]')
    tabs_name = map(unicode.strip, tabs.xpath('@name').extract())
    pp(tabs_name)
    
    for tab in tabs:
      tab_name = tab.xpath('./@name')
      tab_table = tab.xpath('.//table/tbody')
      pp(u"tab_name: " + tab_name.extract_first())

      print "Headers"
      header_nodes = tab_table.xpath('.//tr//th')
      headers = []
      for header_node in header_nodes:
        text = merge_text_list(header_node.xpath('.//text()').extract())
        headers.append( text )

      pp(headers)

      print "Rows" 
      for row_node in tab_table.xpath('.//tr'):
        for node in row_node.xpath('.//td'):
          text_nodes = node.xpath('.//text()')
          text = merge_text_list(text_nodes.extract())
          link_nodes = node.xpath('.//a/@href').extract()
          #yield {'image_urls': link_nodes }
          pp(link_nodes)
          pp(text)

    


