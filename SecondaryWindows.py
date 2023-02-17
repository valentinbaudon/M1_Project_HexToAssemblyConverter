import json
import locale
import sys

from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QMainWindow, QLabel, QMenu, QAction


# Lancement de la fenêtre "Functionning"
def showFunctioningWindow():
    about_dialog = Functionning()
    about_dialog.exec_()


# Lancement de la fenêtre "About"
def showAboutWindow():
    about = About()
    about.exec_()


# Classe définissant la fenêtre "Functionning"
class Functionning(QDialog):
    # constructeur de la classe "Functionning"
    def __init__(self):
        # récupération des initialisations de la classe mère
        super().__init__()

        # paramètres généraux de la fenêtre
        self.setWindowTitle("Fonctionnement de l'application de traduction")
        self.resize(700, 500)
        self.setFixedSize(700, 500)
        icon = QIcon("graphicResources/TemporaryIcon.ico")
        self.setWindowIcon(icon)

        # initialisation des attributs de la classe
        self.menu_Help = None
        self.actionAbout = None
        self.actionAboutFunctioning = None

        # initialisation de l'objet texte
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFontPointSize(11)
        # if MainWindow.language == "fr_FR": # marche pas
        #     JSON_lang = json.load(open("./OtherFiles/text_fr_FR.json"))
        # else:
        #     JSON_lang = json.load(open("./OtherFiles/text_en_EN.json"))
        # self.text_edit.setPlainText(JSON_lang["HowItWorks"])
        self.text_edit.setStyleSheet("background: transparent;")

        # initialisation du layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

    def setupUi(self, Converter):
        # création de la barre de menu
        self.menu_Help = QtWidgets.QMenu(Converter)
        self.menu_Help.setObjectName("menu_Help")

        # Ajout de la section "About"
        self.actionAbout = QtWidgets.QAction(Converter)
        self.actionAbout.setObjectName("actionAbout")
        self.menu_Help.addAction(self.actionAbout)

        # Ajout de la sous-section "Fonctionnement" à la section "About"
        self.actionAboutFunctioning = QtWidgets.QAction(Converter)
        self.actionAboutFunctioning.setObjectName("actionAboutFunctioning")
        self.menu_Help.addAction(self.actionAboutFunctioning)

        # Connexion de la sous-section "Fonctionnement" au slot qui affiche la nouvelle fenêtre
        self.actionAboutFunctioning.triggered.connect(showFunctioningWindow)


# Classe définissant la fenêtre "About"
class About(QDialog):
    # constructeur de la classe "Functionning"
    def __init__(self):
        # récupération des initialisations de la classe mère
        super().__init__()

        # paramètres généraux de la fenêtre
        self.setWindowTitle("À propos")
        self.resize(600, 400)
        self.setFixedSize(600, 400)
        icon = QIcon("graphicResources/TemporaryIcon.ico")
        self.setWindowIcon(icon)

        # initialisation des attributs de la classe
        self.menu_Help = None
        self.actionAbout = None
        self.actionAboutFunctioning = None

        # initialisation de l'objet texte
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFontPointSize(11)
        if locale.getlocale()[0] in ["fr_FR", "en_EN"]:
            JSON_lang = json.load(open("./OtherFiles/text_" + locale.getlocale()[0] + ".json"))
        else:
            JSON_lang = json.load(open("./OtherFiles/text_en_EN.json"))
        self.text_edit.setPlainText(JSON_lang["about"])
        self.text_edit.setStyleSheet("background: transparent;")
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.insertHtml('<img src="./OtherFiles/isen_logo.png">')
        cursor.movePosition(QTextCursor.Start)
        self.text_edit.setTextCursor(cursor)

        # initialisation du layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

    def setupUi(self, Converter):
        # création de la barre de menu
        self.menu_Help = QtWidgets.QMenu(Converter)
        self.menu_Help.setObjectName("menu_Help")

        # Ajout de la section "About"
        self.actionAbout = QtWidgets.QAction(Converter)
        self.actionAbout.setObjectName("actionAbout")
        self.menu_Help.addAction(self.actionAbout)

        # Ajout de la sous-section "Fonctionnement" à la section "About"
        self.actionAboutFunctioning = QtWidgets.QAction(Converter)
        self.actionAboutFunctioning.setObjectName("actionAboutFunctioning")
        self.menu_Help.addAction(self.actionAboutFunctioning)

        # Connexion de la section "About" au slot qui affiche la nouvelle fenêtre
        self.actionAboutFunctioning.triggered.connect(showAboutWindow)
