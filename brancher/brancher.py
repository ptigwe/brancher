# -*- coding: utf-8 -*-
import sys

from aqt import mw
from aqt.qt import *
import aqt
import anki
import anki.collection
from anki.sched import Scheduler
from anki.models import defaultModel,defaultField,defaultTemplate

from goo import Goo
from tatoeba import Tatoeba
from treelib import Node, Tree
from listdialog import ListSelection

class BrancherWidget(QWidget):
    def __init__(self):
        super(BrancherWidget, self).__init__()
        self.initUI()
        self.tree = None

    def initUI(self):
        self.l_w = QWidget(self)
        self.r_u = QWidget(self)
        self.r_l = QWidget(self)
        self.r_s = QSplitter(Qt.Vertical, self)
        self.l_grid = QGridLayout()
        self.m_grid = QHBoxLayout()
        self.splitter = QSplitter(self)

        self.tree_view = QTreeWidget()
        self.root = None
        self.connect(self.tree_view, SIGNAL('itemSelectionChanged()'), self.item_changed)

        self.add_btn = QPushButton('Add')
        self.fin_btn = QPushButton('Finish')
        self.clr_btn = QPushButton('Clear')
        self.add_btn.clicked.connect(self.add_card)
        self.fin_btn.clicked.connect(self.fin_card)
        self.clr_btn.clicked.connect(self.clr_card)

        self.l_grid.addWidget(self.tree_view, 1, 0)
        self.l_grid.addWidget(self.add_btn, 2, 0)
        self.l_grid.addWidget(self.fin_btn, 3, 0)
        self.l_grid.addWidget(self.clr_btn, 3, 1)
        self.l_w.setLayout(self.l_grid)

        self.r_grid_u = QGridLayout()
        w_label = QLabel(u'言葉:')
        i_label = QLabel(u'意味:')
        s_label = QLabel(u'例文:')
        self.w_field = QLabel('')
        self.i_field = QLabel('')
        self.i_field.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.s_field = QLabel('')
        self.s_field.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.r_grid_u.setSpacing(10)
        self.r_grid_u.addWidget(w_label, 1, 0)
        self.r_grid_u.addWidget(self.w_field, 1, 1)
        self.r_grid_u.addWidget(i_label, 2, 0)
        self.r_grid_u.addWidget(self.i_field, 2, 1)
        self.r_grid_u.addWidget(s_label, 3, 0)
        self.r_grid_u.addWidget(self.s_field, 3, 1)
        self.r_u.setLayout(self.r_grid_u)

        self.r_grid_l = QGridLayout()
        w_label = QLabel(u'言葉:')
        i_label = QLabel(u'意味:')
        s_label = QLabel(u'例文:')
        max_size = s_label.sizeHint().height() * 3
        self.w_entry = QLineEdit('')
        self.i_entry = QTextEdit('')
        self.s_entry = QTextEdit('')
        self.i_entry.setMaximumHeight(max_size)
        self.s_entry.setMaximumHeight(max_size)
        self.connect(self.w_entry, SIGNAL('textChanged()'), self.update_fields)
        self.connect(self.i_entry, SIGNAL('textChanged()'), self.update_fields)
        self.connect(self.s_entry, SIGNAL('textChanged()'), self.update_fields)
        self.r_grid_l.setSpacing(10)
        self.r_grid_l.addWidget(w_label, 1, 0)
        self.r_grid_l.addWidget(self.w_entry, 1, 1)
        self.r_grid_l.addWidget(i_label, 2, 0)
        self.r_grid_l.addWidget(self.i_entry, 2, 1)
        self.r_grid_l.addWidget(s_label, 3, 0)
        self.r_grid_l.addWidget(self.s_entry, 3, 1)
        self.r_l.setLayout(self.r_grid_l)
        self.r_s.addWidget(self.r_u)
        self.r_s.addWidget(self.r_l)

        self.splitter.addWidget(self.l_w)
        self.splitter.addWidget(self.r_s)
        self.m_grid.addWidget(self.splitter)
        self.setLayout(self.m_grid)
        self.setGeometry(300, 300, 800, 500)
        self.setWindowTitle('Review')


    def fin_card(self, arg):
        words = [i for i in self.tree.expand_tree(mode=Tree.DEPTH)][::-1]
        for i in words:
            data = self.tree[i].data
            res = {u'Keyword':self.tree[i].tag, u'Expression':data[1], u'Definition':data[0]}
            self.anki.addNote('Brancher', 'BrancherJapanese', res)
        self.clr_card(arg)

    def clr_card(self, arg):
        if self.root is not None:
            self.tree_view.invisibleRootItem().removeChild(self.root)
        self.root = None
        self.tree = None

    def add_card(self, arg):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                'Enter your name:')
        if ok:
            self.add_word(text)

    def add_word(self, text):
        search_res = Goo.search(text)

        ls = ListSelection(search_res[1], "Select the correct word entry", self)
        if ls.exec_() == QDialog.Accepted:
            w_idx = ls.get_value()
            text_res = search_res[1][int(w_idx)].split(u'【')
            if len(text_res) == 2:
                text = text_res[1][:-1]
            definitions = Goo.get_definition(text, link=search_res[0][int(w_idx)])

            ls = ListSelection(definitions, "Select the desired definition", self)
            if ls.exec_() == QDialog.Accepted:
                d_idx = ls.get_value()
                definition = definitions[int(d_idx)]
                sentence = u''
                sen_res = Tatoeba.search(text)

                ls = ListSelection(sen_res, "Select a sample sentence", self)
                if ls.exec_() == QDialog.Accepted:
                    s_idx = ls.get_value()
                    sentence = sen_res[int(s_idx)]

                if self.tree is None:
                    node = QTreeWidgetItem(self.tree_view)
                    node.setText(0, text)
                    self.tree = Tree()
                    text = node.text(0)
                    self.tree.create_node(text, text, data=(definition, sentence))
                    self.root = node
                else:
                    sel = self.tree_view.selectedItems()
                    if len(sel) == 1:
                        sel = sel[0]
                        node = QTreeWidgetItem(sel)
                        node.setText(0, text)
                        text = node.text(0)
                        self.tree.create_node(text, text, parent=sel.text(0),
                                data=(definition,sentence))
                        sel.setExpanded(True)
                        sel.setSelected(False)
                        node.setSelected(True)

    def item_changed(self):
        print self.tree_view.selectedItems()
        for i in self.tree_view.selectedItems():
            self.w_field.setText(i.text(0))
            self.w_entry.setText(i.text(0))
            imi, reibun = self.tree.get_node(i.text(0)).data
            self.i_field.setText(imi)
            self.i_entry.setText(imi)
            self.s_field.setText(reibun)
            self.s_entry.setText(reibun)

    def update_fields(self):
        if len(self.tree_view.selectedItems()) != 1:
            return

        sel = self.tree_view.selectedItems()[0]
        node = self.tree.get_node(sel.text(0))
        node.data = (self.i_entry.toPlainText(), self.s_entry.toPlainText())
        self.i_field.setText(node.data[0])
        self.s_field.setText(node.data[1])

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_B:
            if self.i_field.hasSelectedText():
                self.add_word(self.i_field.selectedText())
            if self.s_field.hasSelectedText():
                self.add_word(self.s_field.selectedText())

def main():
    app = QApplication(sys.argv)
    ex = BrancherWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
