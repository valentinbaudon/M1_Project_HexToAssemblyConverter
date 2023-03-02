from ApplicationWindow import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


Logo = resource_path("graphicResources/TemporaryIcon.ico")

# Initialisation des composantes fenêtres de l'application
app = QtWidgets.QApplication(sys.argv)
HexaToAssemblyConverter = QtWidgets.QMainWindow()
window = MainWindow()

# Affichage et lien des fenêtres crées aux objets et valeurs crées dans le fichier "ApplicationWindow.py"
window.setupUi(HexaToAssemblyConverter)
HexaToAssemblyConverter.show()
sys.exit(app.exec_())
