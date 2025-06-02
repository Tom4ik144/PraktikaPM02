from PyQt5 import QtWidgets
import mysql.connector

conn = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='user08',
            password='36278',
            database='user08'
        ) # подключаемся к базе данных

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