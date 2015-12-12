import sys
from PyQt4.QtGui import *
class ListSelection(QDialog):
    def __init__(self, item_ls, parent=None):
        super(ListSelection, self).__init__(parent)
        self.result = ""
        #================================================= 
        # listbox
        #================================================= 
        self.listWidget = QListWidget()
        self.items = []
        for item in item_ls:
            w_item = QListWidgetItem(item)
            self.items.append(w_item)
            self.listWidget.addItem(w_item)
            self.listWidget.itemClicked.connect(self.OnSingleClick)
            self.listWidget.itemActivated.connect(self.OnDoubleClick)
        layout = QGridLayout()
        row=0
        layout.addWidget(self.listWidget,row,0,1,3) #col span=1, row span=3
        #================================================= 
        # OK, Cancel
        #================================================= 
        row +=1
        self.but_ok = QPushButton("OK")
        layout.addWidget(self.but_ok ,row,1)
        self.but_ok.clicked.connect(self.OnOk)

        self.but_cancel = QPushButton("Cancel")
        layout.addWidget(self.but_cancel ,row,2)
        self.but_cancel.clicked.connect(self.OnCancel)

        #================================================= 
        #
        #================================================= 
        self.setLayout(layout)
        self.setGeometry(300, 200, 460, 350)

    def OnSingleClick(self, item):
        self.result = self.items.index(item)

    def OnDoubleClick(self, item):
        self.result = self.items.index(item)
        self.done(QDialog.Accepted)
        return self.result

    def OnOk(self):
        if self.result == "":
            QMessageBox.information(self, "Error",
            "One item must be selected")
            return 
        self.done(QDialog.Accepted)
        return self.result

    def OnCancel(self):
        self.done(QDialog.Rejected)

    def GetValue(self):
        return self.result

def main():
    app = QApplication(sys.argv)
    ls = ['apples','bananas','melons']
    lb = ListSelection(ls)
    returnCode=lb.exec_()
    print(returnCode)
    value = lb.GetValue()
    print(value)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
