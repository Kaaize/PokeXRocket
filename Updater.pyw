import AutoUpdate
import os
import sys
import subprocess
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import tempfile


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('updater.ui', self) # Load the .ui file
        
        AutoUpdate.set_url("https://raw.githubusercontent.com/Kaaize/PokeXRocket/main/version.txt")
        AutoUpdate.set_download_link("https://github.com/Kaaize/PokeXRocket/raw/main/PxRocket_Setup.exe")
        with open("version.txt", "r") as version:
            AutoUpdate.set_current_version(version.readline())
        self.show() # Show the GUI
        self.update()

        if not AutoUpdate.is_up_to_date():
            self.label.setText("Baixando Atualizações...")
            QtGui.QGuiApplication.processEvents() 
            with tempfile.TemporaryDirectory() as dirpath:
                AutoUpdate.download(rf"{dirpath}/PxRocket_Setup.exe")
                self.label.setText("Atualizando...")
                QtGui.QGuiApplication.processEvents() 
                subprocess.call([rf"{dirpath}/PxRocket_Setup.exe", "/VERYSILENT", "/CURRENTUSER", "/FORCECLOSEAPPLICATIONS", "/SUPPRESSMSGBOXES"])
                self.destroy()
        else:
            self.destroy()
            f = subprocess.call([rf"{os.getcwd()}\PxRocket.exe"])  

        sys.exit()




app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
window.setAttribute(QtCore.Qt.WA_QuitOnClose)