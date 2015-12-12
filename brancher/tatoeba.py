from lxml import html
import requests

class Tatoeba:
    link = u"https://tatoeba.org/eng/sentences/search/page:{0}?query={1}&from=jpn&to=none"
    @staticmethod
    def search(word):
        page = requests.get(Tatoeba.link.format(1, word))
        tree = html.fromstring(page.content)
        res1 = tree.xpath('//div[@class="module"]//div[@lang="ja"]/text()')
        page = requests.get(Tatoeba.link.format(2, word))
        tree = html.fromstring(page.content)
        res2 = tree.xpath('//div[@class="module"]//div[@lang="ja"]/text()')
        return list(set(res1 + res2))
