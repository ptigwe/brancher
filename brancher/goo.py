# -*- coding: utf-8 -*-
from lxml import html
import requests

from HTMLParser import HTMLParser

class GooParser(HTMLParser):
    def __init__(self, li_extra=True):
        HTMLParser.__init__(self)
        self.li_class = 'in-ttl-b'
        if li_extra:
            self.li_class += ' text-indent'
        self.parsing_li = False
        self.ignore = False
        self.data = []
        self.cur = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            at = dict(attrs)
            if 'class' in at and at['class'].startswith(self.li_class):
                #print at
                self.parsing_li = True
        if tag == 'strong' and self.parsing_li:
            self.ignore = True

    def handle_endtag(self, tag):
        if self.parsing_li and tag == 'li':
            self.parsing_li = False
            #print unicode(self.cur, 'utf-8')
            self.data.append(unicode(self.cur, 'utf-8'))
            self.cur = ''
        if self.parsing_li and tag == 'strong' and self.ignore:
            self.ignore = False

    def handle_data(self, data):
        if self.parsing_li and not self.ignore:
            self.cur += data

class Goo:
    prefix = "http://dictionary.goo.ne.jp/"
    @staticmethod
    def search(word):
        page = requests.get(Goo.prefix + "srch/all/" + word + "/m0u")
        tree = html.fromstring(page.content)
        res1 = tree.xpath('//div[@id="NR-main"]//div[@class="section contents-wrap-a-in search"]//ul[@class="list-search-a"]/li//a/@href')
        res2 = tree.xpath(('//div[@id="NR-main"]//div[@class="section contents-wrap-a-in '
                'search"]//ul[@class="list-search-a"]/li//dt[@class="title ' 
                'search-ttl-a"]//text()'))
        r1 = []
        r2 = []
        for i in range(len(res1)):
            if str(res1[i]).startswith('/jn/'):
                r1.append(res1[i])
                r2.append(res2[i])

        return (r1, r2)

    @staticmethod
    def get_definition(word, index = -1, link = None):
        if link is None:
            if index < 0:
                print "Error index should be set if link isn't set"
            links, _ = search(word)
            link = links[index]
        page = requests.get(Goo.prefix + link)
        #tree = html.fromstring(page.content)
        #res1 = tree.xpath(('//div[@class="kokugo"]//li[@class="in-ttl-b '
        #        'text-indent"]/text()'))
        #if len(res1) == 0:
        #    return tree.xpath(('//div[@class="kokugo"]//li[@class="in-ttl-b"]'
        #        '/text()'))
        #return res1
        parser = GooParser('in-ttl-b text-indent' in page.content)
        parser.feed(page.content)
        return parser.data

