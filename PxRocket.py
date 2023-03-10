from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
import os
import json
import subprocess
from time import sleep
import AutoUpdate

with open('crafts.json', 'r') as f:
    crafts = json.load(f)

with open('items.json', 'r') as f:
    items = json.load(f)



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('main.ui', self) # Load the .ui file
        self.searchWindow = uic.loadUi('search.ui')
        self.show() # Show the GUI
        #self.setWindowIcon(QtGui.QIcon(resource_path('icon.ico')))

        self.actionAtualizar.triggered.connect(self.Atualizar)

        self.edtBoost.valueChanged.connect(self.CalcularBoost)
        self.edtAtual.valueChanged.connect(self.CalcularBoost)
        self.edtAlvo.valueChanged.connect(self.CalcularBoost)
        self.edtPreco.valueChanged.connect(self.CalcularBoost)
        self.cbBonus.stateChanged.connect(self.CalcularBoost)
        self.CalcularBoost()
        self.btnCalcular.clicked.connect(self.CreateBoost70)
        self.craftTable.itemChanged.connect(self.CalculaTotal)
        self.edtCraftName.returnPressed.connect(self.CreateBoost70)
        self.edtCraftQty.valueChanged.connect(self.CreateBoost70)
        self.edtItemName.returnPressed.connect(self.SearchUse)

        self.btnUsesList.clicked.connect(self.SearchUse)
        self.searchWindow.btnSelecionar.clicked.connect(self.selecionado)
        #self.edtCraftName.installEventFilter(self)
        self.btnCelebiDecode.clicked.connect(self.CelebiDecoder)

        header = self.craftTable.horizontalHeader()    
        header.resizeSection(0, 500)  
        header.resizeSection(1, 120)  
        header.resizeSection(2, 180)  
        header.resizeSection(3, 220)  

        header = self.usesList.horizontalHeader()       
        header.resizeSection(0, 700)  
        header.resizeSection(1, 100)  

        self.craftAnterior = ''
        self.result = {}
        self.Search()

    def Atualizar(self):
        AutoUpdate.set_url("https://raw.githubusercontent.com/Kaaize/PokeXRocket/main/version.txt")

        with open("version.txt", "r") as version:
            AutoUpdate.set_current_version(version.readline())
        if not AutoUpdate.is_up_to_date():
            subprocess.Popen(['updater.exe'], shell=True)
            sys.exit(0)
        else:
            QtWidgets.QMessageBox.information(self, "Atualizado", "N??o h?? atualiza????es disponiveis.")

    def SearchUse(self):
        try:
            self.usesList.setRowCount(0)
            for key, value in crafts.items():
                if value.get(self.edtItemName.text().lower()):
                    row = self.usesList.rowCount()
                    col = self.usesList.columnCount()
                    self.usesList.insertRow(row)
                    self.usesList.setItem(row-1, col, QtWidgets.QTableWidgetItem(key))
                    self.usesList.setItem(row-1, col+1, QtWidgets.QTableWidgetItem(str(value[self.edtItemName.text().lower()])))
        except Exception as E:
            QtWidgets.QMessageBox.warning(self, "ERRO", str(E))


    def Search(self):
        names = list(crafts.keys())
        model = QtGui.QStandardItemModel(len(names),1)
        model.setHorizontalHeaderLabels(["CRAFT"])

        for row, craft in enumerate(names):
            item = QtGui.QStandardItem(craft)
            model.setItem(row, 0, item)



        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)
        self.searchWindow.edtSearch.textChanged.connect(filter_proxy_model.setFilterRegExp)
        self.searchWindow.searchList.setModel(filter_proxy_model)

        self.searchWindow.searchList.doubleClicked.connect(self.selecionado)

    def selecionado(self):
        model = self.searchWindow.searchList.model()
        item = model.data(self.searchWindow.searchList.currentIndex())
        self.edtCraftName.setText(item)
        self.CreateBoost70()
        self.searchWindow.close()

    def keyPressEvent(self, event):
        foc = QtWidgets.QApplication.focusWidget().objectName()
        if event.key() == QtCore.Qt.Key_F2:
            if foc == 'edtCraftName':
                self.searchWindow.exec_()#show()


    def Calculate(self, craft, qty):
        if not crafts.get(craft):
            return 

        for item,itemqty in crafts[craft].items():
            try:
                price = items[item]
            except:
                price = 0
            if result.get(item):
                result[item]['qty'] += itemqty*qty
                #result[item]['price'] = price
            else:
                result[item] = {'qty': itemqty*qty, 'price': price}

            self.Calculate(item, itemqty*qty)
        return result
        
    def CreateBoost70(self):
        global result
        result = {}
        craft = self.edtCraftName.text().lower()
        
        qty = self.edtCraftQty.value()
        if qty < 1:
            qty = 1
        else:
            qty= int(qty)
        infos = self.Calculate(craft, qty)
        if not infos:
            self.searchWindow.show()
            return
        if infos == -1:
            return
        if self.craftAnterior == craft:
            count = 0
            for i in reversed(infos):
                self.craftTable.item(count, 1).setText(f"{infos[i]['qty']:.2f}")
                count += 1
            self.CalculaTotal
            return
        else:
            self.craftTable.setRowCount(0)
        row = self.craftTable.rowCount()
        col = self.craftTable.columnCount()
        for i, (k, v) in enumerate(infos.items()):
            try:
                icon = QtGui.QIcon(f'icons/{k}.png')
            except:
                pass
            self.craftTable.insertRow(row)
            self.craftTable.setItem(row-1, col, QtWidgets.QTableWidgetItem(icon, k))
            self.craftTable.setItem(row-1, col+1, QtWidgets.QTableWidgetItem(f"{v['qty']:.2f}"))
            self.craftTable.setItem(row-1, col+2, QtWidgets.QTableWidgetItem(f"{v['price']:.2f}"))            
            self.craftTable.setItem(row-1, col+3, QtWidgets.QTableWidgetItem(f"{v['qty']*v['price']:.2f}"))
            self.CalculaTotal()
            pass
        self.craftAnterior = craft

    def CalculaTotal(self):
        try:
            total = 0
            for i in range(self.craftTable.rowCount()):
                qty = self.craftTable.item(i, 1).text()
                price = self.craftTable.item(i, 2).text()
                soma = float(qty)*float(price)
                total += soma

                self.craftTable.item(i,3).setText(f"{soma:.2f}")
            self.edtTotal.setValue(total)
        except Exception as E:
            print(E)
            QtWidgets.QMessageBox.warning(self, "Erro","H?? um caractere invalido nos campos de N??meros")

    def CalcularBoost(self):
        bonus = self.cbBonus.isChecked()
        atual = self.edtAtual.value()
        target = self.edtAlvo.value()
        increase = self.edtBoost.value()
        preco = self.edtPreco.value()
        result = self.GetStones(increase, target, bonus)-self.GetStones(increase, atual, bonus)
        self.edtStones.setValue(result)
        self.edtPrecoTotal.setValue(result*preco)


    def GetStones(self, increase, target, bonus) -> int:
        stones = 0
        skip = 0
        for i in range(0,target):
            if skip:
                skip -= 1
                continue
            stones += 1+(i//increase)
            if bonus == True and i < 9:
                skip += 1
        return stones
        
    def CelebiDecoder(self) -> str:
        for i in range(5):
            rx = self.findChild(QtWidgets.QSpinBox, f"edtCelebiRX{i+1}")
            ry = self.findChild(QtWidgets.QSpinBox, f"edtCelebiRY{i+1}")
            rx.setValue(0)
            ry.setValue(0)
        if self.edtCelebiCod.text() == '':
            return

        try:
            startx = self.edtCelebiX.value()
            starty = self.edtCelebiY.value()
            code = self.edtCelebiCod.text()
            posx = []
            posy = []
            var = ''
            for i in range(0,len(code)):
                if not code[i].isdigit():
                    posx.append(code[i])
                    if i != 0:
                        posy.append(var)
                    var = ''
                else:
                    var += code[i]
            posy.append(var)
            code = posx,posy
            coords = []
            for i in range(5):

                x = ord(code[0][i])-96-1
                y = int(code[1][i])-1
                rx = self.findChild(QtWidgets.QSpinBox, f"edtCelebiRX{i+1}")
                ry = self.findChild(QtWidgets.QSpinBox, f"edtCelebiRY{i+1}")
                rx.setValue(startx+x)
                ry.setValue(starty+y)
                coords.append(f"X: {startx+x} Y: {starty+y}")
            
        except:
            QtWidgets.QMessageBox.warning(self, "Erro", "N??o foi poss??vel decodificar corretamente esse c??digo.\n verifique as informa????es e tente novamente")

            
    

    
app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application