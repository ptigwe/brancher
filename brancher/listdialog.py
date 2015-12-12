# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
class ListSelection(QDialog):
    def __init__(self, item_ls, title="", parent=None):
        super(ListSelection, self).__init__(parent)
        self.setWindowTitle(title)
        self.result = ""

        self.listWidget = QListWidget()
        self.items = []
        for item in item_ls:
            w_item = QListWidgetItem(item)
            self.items.append(w_item)
            self.listWidget.addItem(w_item)
            self.listWidget.itemClicked.connect(self.single_click)
            self.listWidget.itemActivated.connect(self.double_click)
        layout = QGridLayout()
        row=0
        layout.addWidget(self.listWidget,row,0,1,3) #col span=1, row span=3

        row +=1
        self.but_ok = QPushButton("OK")
        layout.addWidget(self.but_ok ,row,1)
        self.but_ok.clicked.connect(self.ok)

        self.but_cancel = QPushButton("Cancel")
        layout.addWidget(self.but_cancel ,row,2)
        self.but_cancel.clicked.connect(self.cancel)

        self.setLayout(layout)
        self.setGeometry(300, 200, 460, 350)

    def single_click(self, item):
        self.result = self.items.index(item)

    def double_click(self, item):
        self.result = self.items.index(item)
        self.done(QDialog.Accepted)
        return self.result

    def ok(self):
        if self.result == "":
            QMessageBox.information(self, "Error",
            "One item must be selected")
            return 
        self.done(QDialog.Accepted)
        return self.result

    def cancel(self):
        self.done(QDialog.Rejected)

    def get_value(self):
        return self.result
