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

        self.show() # Show the GUI
        self.update()
        AutoUpdate.set_download_link("https://github.com/Kaaize/PokeXRocket/raw/main/PxRocket_Setup.exe")
        self.label.setText("Baixando Atualizações...")
        QtGui.QGuiApplication.processEvents() 

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as dirpath:
            AutoUpdate.download(rf"{dirpath}/PxRocket_Setup.exe")
            self.label.setText("Atualizando...")
            QtGui.QGuiApplication.processEvents() 
            subprocess.Popen([rf"{dirpath}/PxRocket_Setup.exe", "/VERYSILENT", "/CURRENTUSER", "/FORCECLOSEAPPLICATIONS", "/SUPPRESSMSGBOXES"])
            self.destroy()
        sys.exit()




app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
