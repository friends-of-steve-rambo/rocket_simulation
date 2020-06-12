# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys


def menu():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()

    r_planet = float(ui.plainTextEdit.toPlainText()) * 10**6
    Mp = float(ui.plainTextEdit_2.toPlainText()) * 10**24
    dry_mass = float(ui.plainTextEdit_4.toPlainText())  # 5000 кг
    fuel_mass = float(ui.plainTextEdit_3.toPlainText())  # 10000 кг
    u = float(ui.plainTextEdit_5.toPlainText())  # 5000 м\c Скорость истечения топлива, удельный импульс
    m_t = float(ui.plainTextEdit_6.toPlainText())  # 15 расход топлива кг\с
    orbit = ui.checkBox.isChecked()
    return r_planet, Mp, dry_mass, fuel_mass, u, m_t, orbit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("[351819] Симуляция запуска ракеты")
        MainWindow.resize(362, 505)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(210, 130, 141, 20))
        self.label_6.setObjectName("label_6")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 40, 121, 20))
        self.label_3.setObjectName("label_3")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(10, 270, 201, 25))
        self.checkBox.setObjectName("checkBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 450, 201, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.click)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 190, 161, 20))
        self.label_7.setObjectName("label_7")
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(20, 150, 101, 31))
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(210, 150, 111, 31))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 310, 341, 111))
        self.textBrowser.setObjectName("textBrowser")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(210, 190, 141, 20))
        self.label_8.setObjectName("label_8")
        self.plainTextEdit_5 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_5.setGeometry(QtCore.QRect(20, 210, 101, 31))
        self.plainTextEdit_5.setObjectName("plainTextEdit_5")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(210, 60, 111, 31))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 20, 181, 20))
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 130, 111, 20))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(80, 110, 181, 20))
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 111, 20))
        self.label_2.setObjectName("label_2")
        self.plainTextEdit_6 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_6.setGeometry(QtCore.QRect(210, 210, 111, 31))
        self.plainTextEdit_6.setObjectName("plainTextEdit_6")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 60, 101, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "[351819 Симуляция запуска ракеты]"))
        self.label_6.setText(_translate("MainWindow", "Масса  топлива, кг"))
        self.label_3.setText(_translate("MainWindow", "Масса, (10^24)кг"))
        self.checkBox.setText(_translate("MainWindow", "Запуск на орбите (100км)"))
        self.pushButton.setText(_translate("MainWindow", "Запустить симуляцию"))
        self.label_7.setText(_translate("MainWindow", "Удельный импульс, м/c"))
        self.plainTextEdit_4.setPlainText(_translate("MainWindow", "5000"))
        self.plainTextEdit_3.setPlainText(_translate("MainWindow", "10000"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Выполнил: Агеев П.А.</p>\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ст. гр. 351819</p>\n"
"<p align=\"right\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Преподаватель:</p>\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Василишин И.И.</p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "Расход топлива, кг/c"))
        self.plainTextEdit_5.setPlainText(_translate("MainWindow", "5000"))
        self.plainTextEdit_2.setPlainText(_translate("MainWindow", "0.0735"))
        self.label.setText(_translate("MainWindow", "Характеристики планеты"))
        self.label_5.setText(_translate("MainWindow", "\"Сухая\" масса, кг"))
        self.label_4.setText(_translate("MainWindow", "Характеристики ракеты"))
        self.label_2.setText(_translate("MainWindow", "Радиус, (10^6)м"))
        self.plainTextEdit_6.setPlainText(_translate("MainWindow", "15"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "1.738"))

    def click(self):
        QtCore.QCoreApplication.instance().quit()