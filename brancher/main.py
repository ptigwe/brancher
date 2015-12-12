#!/usr/bin/env python

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
