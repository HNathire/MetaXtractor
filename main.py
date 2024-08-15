import sys
from gui import Gui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import os

hiddenimports = ['firebase_admin']

def main():
    app = QApplication(sys.argv)
    gui = Gui()
    gui.setWindowTitle("MetaXtract")
    
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    
    # Specify the relative path to the icon file
    icon_path = os.path.join(script_dir, "icon.ico")
    
    gui.setWindowIcon(QIcon(icon_path))
    gui.show()
    app.exec()

if __name__ == "__main__":
    main()