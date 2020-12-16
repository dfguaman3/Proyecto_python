import requests,json,urllib.request, datetime, sys
import pandas as pd
from PyQt5 import uic, QtWidgets
from mplwidget import MplWidget
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson'
url_covid = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
#url= 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
qtCreatorFile = "interfaz.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.MplWidget = MplWidget(self.MplWidget)
        self.cargar.clicked.connect(self.getCSV)
        
        self.graficar.clicked.connect(self.presentarTabla)
        self.estadistica.clicked.connect(self.estadisticas)
    
    def getCSV(self):
        '''
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if filePath != "":
            print ("Dirección",filePath) #Opcional imprimir la dirección del archivo
            self.df = pd.read_csv(str(filePath))
        '''
        if self.cargar.isClicked():
            self.estado.setText("Loading data")
        self.df = pd.read_csv(url_covid)#, parse_dates=['date'], index_col='date')
        while True:
            if self.df.empty:
                self.estado.setText("Loading data")
            else:
                self.estado.setText("Ready")
            break
        self.combox.addItems(list(self.df.columns.values))
        self.comboy.addItems(list(self.df.columns.values))
        self.combostack.addItems(list(self.df.columns.values))
        
    def plot(self):
        x = self.df[str(self.combox.currentText())]
        y = self.df[str(self.comboy.currentText())]
        plt.plot(x,y)
        plt.show()
        
        
    def estadisticas(self):
        estatics= "Estadisticas location: "+str(self.combostack.currentText())+str(self.df[self.combostack.currentText()].describe())
        self.resultado.setText(estatics)

    def presentarTabla(self):
        try:
            
            name_a = 'Fecha'
            name_b = 'Pais'
            name_c = 'Casos'
            name_d= 'Muertes'
            self.a = name_a
            self.b = name_b
            self.c = name_c
            self.d = name_d
            lista_date = []
            lista_country =[]
            lista_cases = []
            lista_deaths= []
            data = pd.read_csv(url_covid, index_col = 0,header = 0)
            Long = 20#len(data['date'])
            for i in range(Long):
                date=data['date'][i]
                country=data['location'][i]
                cases=data['total_cases'][i]
                deaths=data['total_deaths'][i]
                lista_date += [date]
                lista_country +=[country]
                lista_cases += [cases]
                lista_deaths += [deaths]
                print(lista_date)
            self.tableWidget.setRowCount(Long)
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setHorizontalHeaderLabels([name_a,name_b,name_c,name_d])
            self.lon = range(1,len(lista_date)+1)
            for row in range(Long):
                contentCell = str(lista_date[row])
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(contentCell))
                contentCell = str(lista_country[row])
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(contentCell))
                contentCell = str(lista_cases[row])
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(contentCell))
                contentCell = str(lista_deaths[row])
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(contentCell))

            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.bar(list(self.lon),lista_cases, width = 0.4, align='center')
            self.MplWidget.canvas.axes.legend((self.c, self.d), loc='upper right')
            self.MplWidget.canvas.axes.set_title(f'{self.c} - {self.d}')
            self.MplWidget.canvas.axes.set_xlabel('Fecha')
            self.MplWidget.canvas.axes.set_ylabel('Numero de casos diarios')
            self.MplWidget.canvas.axes.grid(True)
            self.MplWidget.canvas.draw()     
            
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
