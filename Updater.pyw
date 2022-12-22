import AutoUpdate
import os
import sys
import subprocess
from PyQt5 import QtWidgets, uic
from time import sleep



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('updater.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.update()

        AutoUpdate.set_url("https://raw.githubusercontent.com/Kaaize/PokeXRocket/main/version.txt")

        AutoUpdate.set_download_link("https://github.com/Kaaize/PokeXRocket/raw/main/PxRocket.exe")

        with open("version.txt", "r") as version:
            AutoUpdate.set_current_version(version.readline())



            if not AutoUpdate.is_up_to_date():
                self.label.setText("Atualizando...")
                self.label.update()
                AutoUpdate.download(os.getcwd()+'\\PxRocket.exe')
            else:
                self.destroy()
                subprocess.call([rf"{os.getcwd()}\PxRocket.exe"])




app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
