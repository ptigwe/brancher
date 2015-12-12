# -*- coding: utf-8 -*-

# Copyright (C) 2015 Tobenna Peter Igwe.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
