# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_table.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_choose_table(object):
    def setupUi(self, choose_table):
        choose_table.setObjectName("choose_table")
        choose_table.resize(400, 60)
        choose_table.setMinimumSize(QtCore.QSize(400, 60))
        choose_table.setMaximumSize(QtCore.QSize(400, 60))
        self.gridLayout = QtWidgets.QGridLayout(choose_table)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(choose_table)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.choose_grocery_setBtn = QtWidgets.QPushButton(choose_table)
        self.choose_grocery_setBtn.setObjectName("choose_grocery_setBtn")
        self.gridLayout.addWidget(self.choose_grocery_setBtn, 1, 0, 1, 1)
        self.choose_productBtn = QtWidgets.QPushButton(choose_table)
        self.choose_productBtn.setObjectName("choose_productBtn")
        self.gridLayout.addWidget(self.choose_productBtn, 1, 1, 1, 1)

        self.retranslateUi(choose_table)
        QtCore.QMetaObject.connectSlotsByName(choose_table)

    def retranslateUi(self, choose_table):
        _translate = QtCore.QCoreApplication.translate
        choose_table.setWindowTitle(_translate("choose_table", "Выбор"))
        self.label.setText(_translate("choose_table", "Выберите таблицу для изменения"))
        self.choose_grocery_setBtn.setText(_translate("choose_table", "Продуктовый набор"))
        self.choose_productBtn.setText(_translate("choose_table", "Продукты"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    choose_table = QtWidgets.QWidget()
    ui = Ui_choose_table()
    ui.setupUi(choose_table)
    choose_table.show()
    sys.exit(app.exec_())
