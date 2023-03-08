from ApplicationWindow import *


# Fonction pour récupérer le path des fichiers
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Permet de récupérer le logo pour la génération de l'exécutable
Logo = resource_path("graphicResources/TemporaryIcon.ico")

# Initialisation des composantes fenêtres de l'application
app = QtWidgets.QApplication(sys.argv)
HexaToAssemblyConverter = QtWidgets.QMainWindow()
window = MainWindow()

# Affichage et lien des fenêtres créés aux objets et valeurs créés dans le fichier "ApplicationWindow.py"
window.setupUi(HexaToAssemblyConverter)
HexaToAssemblyConverter.show()
sys.exit(app.exec_())
