from ApplicationWindow import *

# Initialisation des composantes fenêtres de l'applications
app = QtWidgets.QApplication(sys.argv)
HexaToAssemblyConverter = QtWidgets.QMainWindow()
window = MainWindow()

# Affichage et lien des fenêtres crées aux objets et valeurs crées dans le fichier "ApplicationWindow.py"
window.setupUi(HexaToAssemblyConverter)
HexaToAssemblyConverter.show()
sys.exit(app.exec_())
