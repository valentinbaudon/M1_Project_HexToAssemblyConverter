import json
import locale
import sys
from PyQt5 import QtWidgets, QtCore, Qt, QtGui
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QMainWindow, QLabel, QMenu, QAction


# Classe définissant la fenêtre "Functionning"
class Functionning(QDialog):
    # constructeur de la classe "Functionning"
    def __init__(self, langue):
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
        if langue == "fr_FR":
            JSON_lang = json.load(open("./OtherFiles/text_fr_FR.json"))
        else:
            JSON_lang = json.load(open("./OtherFiles/text_en_EN.json"))
        self.text_edit.setPlainText(JSON_lang["HowItWorks"])
        self.text_edit.setStyleSheet("background: transparent;")

        # initialisation du layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)


# Classe définissant la fenêtre "About"
class About(QDialog):
    # constructeur de la classe "Functionning"
    def __init__(self, langue):
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
        if langue == "fr_FR":
            JSON_lang = json.load(open("./OtherFiles/text_fr_FR.json"))
        else:
            JSON_lang = json.load(open("./OtherFiles/text_en_EN.json"))
        self.text_edit.setPlainText(JSON_lang["about"])
        self.text_edit.setStyleSheet("background: transparent;")

        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.insertHtml('<img src="graphicResources/isen_logo.png">')
        cursor.movePosition(QTextCursor.Start)
        self.text_edit.setTextCursor(cursor)

        # initialisation du layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
