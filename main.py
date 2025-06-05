''' импорт модулей '''
import sys
from PyQt5 import QtWidgets
import mysql.connector
import Supermarket
import add_product
import choose_table
import add_product_to_GS

class Kassa(QtWidgets.QWidget, Supermarket.Ui_Kassa):
    ''' Запуск интерфейса''' 
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
        self.addButton.clicked.connect(self.choose_table)
        self.clearButton.clicked.connect(self.clear_set)

    def load_grocery_set_data(self):
        ''' Загрузка данных из БД '''
        cursor = self.conn.cursor()
        cursor.execute('''SELECT P.name_product, GS.numbers_product
                          FROM Grosery_set GS
                          JOIN product P ON GS.ID_product = P.ID_product;''')

        self.GrocerySetTable.setRowCount(0)
        row_position_grosery_set = 0

        for one_row in cursor:
            self.GrocerySetTable.insertRow(row_position_grosery_set)
            self.GrocerySetTable.setItem(row_position_grosery_set, 0, 
            QtWidgets.QTableWidgetItem(one_row[0]))
            self.GrocerySetTable.setItem(row_position_grosery_set, 1, 
            QtWidgets.QTableWidgetItem(str(one_row[1])))
            row_position_grosery_set += 1

        cursor1 = self.conn.cursor()
        cursor1.execute('''SELECT name_product, price, weight FROM product''')

        self.productTable.setRowCount(0)
        row_position_product = 0

        for two_row in cursor1:
            self.productTable.insertRow(row_position_product)
            self.productTable.setItem(row_position_product, 0, 
            QtWidgets.QTableWidgetItem(two_row[0]))
            self.productTable.setItem(row_position_product, 1, 
            QtWidgets.QTableWidgetItem(str(two_row[1])))
            self.productTable.setItem(row_position_product, 2, 
            QtWidgets.QTableWidgetItem(str(two_row[2])))
            row_position_product += 1

    def choose_table(self):
        ''' Запуск выбора таблицы '''
        self.add_product = ChooseTable(parent=self)  # Передаём ссылку на главное окно
        self.add_product.show()

    def clear_set(self):
        ''' Очищение продуктового набора '''
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Grosery_set")
        self.conn.commit()
        self.load_grocery_set_data()

class ChooseTable(QtWidgets.QWidget, choose_table.Ui_choose_table):
    ''' Выбор таблиц '''
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.choose_productBtn.clicked.connect(self.choose_product)
        self.choose_grocery_setBtn.clicked.connect(self.choose_gs)
    def choose_product(self):
        ''' Выбор добавление товаров в таблицу продукты '''
        self.add_product = AddProduct(parent=self.parent, conn=self.parent.conn)
        self.add_product.show()
        self.hide()
    def choose_gs(self):
        ''' Выбор добавление товаров в таблицу продуктовый набор '''
        self.gs = AddProductToGS(parent=self.parent, conn=self.parent.conn)
        self.gs.show()
        self.hide()

class AddProduct(QtWidgets.QDialog, add_product.Ui_AddProductDialog):
    ''' Добавление товаров в таблицу товаров '''
    def __init__(self, parent=None, conn=None):
        # Ссылка на главное окно и подключение оттуда же (parent и conn)
        super().__init__()
        self.parent = parent
        self.conn = conn
        self.setupUi(self)
        self.addButton.clicked.connect(self.add_product_to_db)

    def add_product_to_db(self):
        ''' Добавление продуктов в таблицу продуктов '''
        name = self.nameInput.text()
        price = self.priceInput.value()
        weight = self.weightInput.value()

        cursor=self.conn.cursor()
        cursor.execute("INSERT INTO product (name_product, price, weight) VALUES (%s, %s, %s)"
        , (name, price, weight))

        self.conn.commit()
        self.parent.load_grocery_set_data() # обновляем данные в главном окне
        self.hide()

class AddProductToGS(QtWidgets.QDialog, add_product_to_GS.Ui_AddToGrocerySetDialog):
    ''' Добавление товаров в таблицу продуктового набора '''
    def __init__(self, parent=None, conn=None):
        super().__init__()
        self.parent = parent
        self.conn = conn
        self.setupUi(self)

        self.load_products_to_combobox()
        self.addButton.clicked.connect(self.add_product_gs)

    def load_products_to_combobox(self):
        ''' Загрузка продуктов в выбор для добавления '''
        cursor = self.conn.cursor()
        cursor.execute("SELECT name_product FROM product")

        self.productComboBox.clear()

        for product in cursor:
            self.productComboBox.addItem(str(product[0]))
    def add_product_gs(self):
        ''' Добавление продуктов в таблицу продуктового набора '''
        name_product_add = self.productComboBox.currentText()
        quantity_product = self.quantitySpinBox.value()

        cursor = self.conn.cursor()
        cursor.execute("SELECT ID_product FROM product WHERE name_product = %s", 
        (name_product_add,))
        product_id = cursor.fetchone()[0]

        cursor.execute('''INSERT INTO Grosery_set (ID_product, numbers_product)
                        VALUES (%s, %s)''', (product_id, quantity_product))
        self.conn.commit()

        self.parent.load_grocery_set_data()
        self.hide()

def main():
    ''' Запуска приложения '''
    application = QtWidgets.QApplication(sys.argv)
    windows = Kassa()
    windows.show()
    application.exec_()

if __name__ == "__main__":
    main()
