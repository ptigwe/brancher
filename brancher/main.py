#!/usr/bin/env python
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

import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, 'treelib'))

from goo import Goo
from treelib import Node, Tree

def main():
    import sys  
    reload(sys)  
    sys.setdefaultencoding('utf8')

    s = raw_input()
    tree = None
    while s != "Done":
        search_res = Goo.search(s)
        for i in range(len(search_res[1])):
            print i, search_res[1][i]
        idx = int(raw_input())
        definition = Goo.get_definition(s, link=search_res[0][idx])
        for i in range(len(definition)):
            print i, definition[i]
        def_idx = int(raw_input())
        if tree is not None:
            tree.show()
            parent = raw_input()
            tree.create_node(s, s, parent=parent)
        else:
            tree = Tree()
            tree.create_node(s, s)
        s = raw_input()

if __name__ == '__main__':
    main()
