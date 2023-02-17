from PyQt5 import QtWidgets

from ApplicationWindow import *

# Initialisation des composantes fenêtres de l'application
app = QtWidgets.QApplication(sys.argv)
HexaToAssemblyConverter = QtWidgets.QMainWindow()
window = MainWindow()

# Affichage et lien des fenêtres crées aux objets et valeurs crées dans le fichier "ApplicationWindow.py"
window.setupUi(HexaToAssemblyConverter)
HexaToAssemblyConverter.show()
sys.exit(app.exec_())
