## Запомнить это нужно!!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import Supermarket
import add_product
import choose_table
import add_product_to_GS
import mysql.connector

class kassa(QtWidgets.QWidget, Supermarket.Ui_Kassa): 
    def __init__(self):
        super().__init__()
        self.setupUi(self) # запускаем интерфейс

        self.conn = mysql.connector.connect(
            host='192.168.15.101',
            port='3306',
            user='user08',
            password='36278',
            database='user08'
        ) # подключаемся к базе данных

        self.load_grocery_set_data()

    def load_grocery_set_data(self):
        cursor = self.conn.cursor() # создаём курсор, который будет считывать данные 
        cursor.execute('''SELECT P.name_product, GS.numbers_product
                          FROM Grosery_set GS
                          JOIN product P ON GS.ID_product = P.ID_product;''')

        self.GrocerySetTable.setRowCount(0)
        rowPositionGrosery_set = 0

        for one_row in cursor:
            self.GrocerySetTable.insertRow(rowPositionGrosery_set)
            self.GrocerySetTable.setItem(rowPositionGrosery_set, 0, QtWidgets.QTableWidgetItem(str(one_row[0])))
            self.GrocerySetTable.setItem(rowPositionGrosery_set, 1, QtWidgets.QTableWidgetItem(str(one_row[1])))
            rowPositionGrosery_set += 1

        cursor1 = self.conn.cursor()
        cursor1.execute('''SELECT name_product, price, weight FROM product''')

        self.productTable.setRowCount(0)
        rowPositionProduct = 0

        for two_row in cursor1:
            self.productTable.insertRow(rowPositionProduct)
            self.productTable.setItem(rowPositionProduct, 0, QtWidgets.QTableWidgetItem(str(two_row[0])))
            self.productTable.setItem(rowPositionProduct, 1, QtWidgets.QTableWidgetItem(str(two_row[1])))
            self.productTable.setItem(rowPositionProduct, 2, QtWidgets.QTableWidgetItem(str(two_row[2])))
            rowPositionProduct += 1

        self.addButton.clicked.connect(self.add_product)
        
        self.clearButton.clicked.connect(self.clear_set)

    def add_product(self):
        self.addProduct = chooseTable() 
        self.addProduct.show()


    def clear_set(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Grosery_set")
        self.conn.commit()
        self.load_grocery_set_data()




class addProduct(QtWidgets.QDialog, add_product.Ui_AddProductDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.addButton.clicked.connect(self.add_product_to_db)

    def add_product_to_db(self):
        name = self.nameInput.text()
        price = self.priceInput.value()
        weight = self.weightInput.value()

        self.conn = mysql.connector.connect(
                host='192.168.15.101',
                port='3306',
                user='user08',
                password='36278',
                database='user08'
            )

        cursor=self.conn.cursor()
        cursor.execute("INSERT INTO product (name_product, price, weight) VALUES (%s, %s, %s) ", (name, price, weight))

        self.conn.commit()
        self.parent.load_grocery_set_data()
        self.hide()



class chooseTable(QtWidgets.QWidget, choose_table.Ui_choose_table):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.choose_productBtn.clicked.connect(self.chooseProduct)
        self.choose_grocery_setBtn.clicked.connect(self.chooseGS)

    def chooseProduct(self):
        self.addProduct = addProduct()
        self.addProduct.show()
        self.hide()
 
    def chooseGS(self):
        self.GS = addProductToGS()
        self.GS.show()
        self.hide()

class addProductToGS(QtWidgets.QDialog, add_product_to_GS.Ui_AddToGrocerySetDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.conn = mysql.connector.connect(
            host='192.168.15.101',
            port='3306',
            user='user08',
            password='36278',
            database='user08'
        )

        self.load_products_to_combobox()
        self.addButton.clicked.connect(self.add_product_GS)

    def load_products_to_combobox(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name_product FROM product")
        
        self.productComboBox.clear()
        
        for product in cursor:
            self.productComboBox.addItem(str(product[0]))

    def add_product_GS(self):
        name_product_add = self.productComboBox.currentText()
        quantity_product = self.quantitySpinBox.value()

    
        cursor = self.conn.cursor()
        cursor.execute("SELECT ID_product FROM product WHERE name_product = %s", (name_product_add,))
        product_id = cursor.fetchone()[0]
        
        cursor.execute('''INSERT INTO Grosery_set (ID_product, numbers_product) 
                        VALUES (%s, %s)''', (product_id, quantity_product))
        self.conn.commit()
        self.load_products_to_combobox()
        self.hide()

        

def main():
    application = QtWidgets.QApplication(sys.argv)
    windows = kassa()
    windows.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    main()