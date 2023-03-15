# Projet M1
# Valentin BAUDON et Hugo MERLE
# ISEN Nantes

import json
import locale
import os
import sys
from PyQt5 import QtWidgets, QtCore, Qt, QtGui
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QMainWindow, QLabel, QMenu, QAction, QButtonGroup

from conversionHexToAssembly import *


# Fonction pour récupérer le path des fichiers
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Classe définissant la fenêtre "Functionning"
class Functionning(QDialog):
    # constructeur de la classe "Functionning"
    def __init__(self, langue):
        # récupération des initialisations de la classe mère
        super().__init__()

        # paramètres généraux de la fenêtre
        self.JSON_lang = json.load(open(resource_path("OtherFiles\\text_" + langue + ".json")))
        self.setWindowTitle(self.JSON_lang["TitleFonctionnement"])
        self.resize(700, 520)
        self.setFixedSize(700, 520)
        icon = QIcon(resource_path("graphicResources/ApplicationIcon.ico"))
        self.setWindowIcon(icon)

        # initialisation des attributs de la classe
        self.menu_Help = None
        self.actionAbout = None
        self.actionAboutFunctioning = None

        # initialisation de l'objet texte
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFontPointSize(11)
        self.text_edit.setPlainText(self.JSON_lang["HowItWorks"])
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
        self.JSON_lang = json.load(open(resource_path("OtherFiles\\text_" + langue + ".json")))
        self.setWindowTitle(self.JSON_lang["actionAbout"])
        self.resize(650, 520)
        self.setFixedSize(650, 520)
        icon = QIcon(resource_path("graphicResources/ApplicationIcon.ico"))
        self.setWindowIcon(icon)

        # initialisation des attributs de la classe
        self.menu_Help = None
        self.actionAbout = None
        self.actionAboutFunctioning = None

        # initialisation et configuration de l'objet texte
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFontPointSize(11)
        self.text_edit.setPlainText(self.JSON_lang["about"])
        self.text_edit.setStyleSheet("background: transparent;")
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.insertHtml('<img src="graphicResources\\isen_logo.png">')
        cursor.movePosition(QTextCursor.Start)
        self.text_edit.setTextCursor(cursor)

        # initialisation du layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)


# Classe définissant la fenêtre "Conversion simple"
class SConversion(QDialog):
    # constructeur de la classe "SConversion"
    def __init__(self, langue):
        # récupération des initialisations de la classe mère
        super().__init__()

        # initialisation des attributs de la classe par défaut
        self.instruction = None
        self.selected_OptionConversion = None
        self.selected_typeInstruction = None
        self.TypeInstruction_Group = None
        self.ConvertedInstructionText = None
        self.ResultTitle = None
        self.ResultConversionLayout = None
        self.ConvertButton = None
        self.ConvertButtonLayout = None
        self.RawInstructionText = None
        self.InsertInstructionTittle = None
        self.InsertInstructionLayout = None
        self.IntegralOption = None
        self.ClassiqueOption = None
        self.CompactOption = None
        self.ConversionOptionsTitle = None
        self.ConversionOptionsLayout = None
        self.BinaryInstruction = None
        self.HexadecimalInstruction = None
        self.InstructionTypeTitle = None
        self.InstructionOptionsLayout = None
        self.GlobalOptionsLayout = None
        self.Title = None
        self.TitleLayout = None
        self.GlobalLayout = None
        self.JSON_lang = json.load(open(resource_path("OtherFiles\\text_" + langue + ".json")))

        # Initialisation de l'option de conversion sélectionnée par défaut
        self.selected_OptionConversion = QtWidgets.QRadioButton()
        self.selected_OptionConversion.setText("Compact")

    # Partie initialisation des textes et noms des éléments de la fenêtre
    def NameInit(self):
        _translate = QtCore.QCoreApplication.translate
        self.Title.setText(_translate("SimpleCWindow", self.JSON_lang["SC_Title"]))
        self.InstructionTypeTitle.setText(_translate("SimpleCWindow", self.JSON_lang["SC_InstructionType"]))
        self.HexadecimalInstruction.setText(_translate("SimpleCWindow", self.JSON_lang["SC_HexaInstruction"]))
        self.BinaryInstruction.setText(_translate("SimpleCWindow", self.JSON_lang["SC_BinaryInstruction"]))
        self.ConversionOptionsTitle.setText(_translate("SimpleCWindow", self.JSON_lang["SC_ConversionOptionTitle"]))
        self.CompactOption.setText(_translate("SimpleCWindow", self.JSON_lang["CompactOption"]))
        self.ClassiqueOption.setText(_translate("SimpleCWindow", self.JSON_lang["ClassiqueOption"]))
        self.IntegralOption.setText(_translate("SimpleCWindow", self.JSON_lang["IntegralOption"]))
        self.InsertInstructionTittle.setText(_translate("SimpleCWindow", self.JSON_lang["SC_InsertInstructionTitle"]))
        self.ConvertButton.setText(_translate("SimpleCWindow", self.JSON_lang["convertButton"]))
        self.ResultTitle.setText(_translate("SimpleCWindow", self.JSON_lang["SC_resultConversionTitle"]))

    # Fonction permettant de mettre à jour le bouton de type d'instruction sélectionnée
    def store_TypeInstruction(self, button):
        self.selected_typeInstruction = button

    # Fonction permettant de mettre à jour le bouton d'option d'affichage sélectionnée
    def store_OptionConversion(self, button):
        self.selected_OptionConversion = button

    # Fonction permettant de faire la traduction du fichier hexa et de mettre le résultat dans le fichier "Assembly.txt"
    def translate(self):
        self.instruction = self.RawInstructionText.toPlainText()

        # Gestion d'erreur si pas de type d'instruction sélectionné
        if self.selected_typeInstruction is None:
            with open(resource_path("ConversionFiles\\Assembly.txt"), "w") as f:
                f.write("ERROR : no instruction type selected")
            f.close()

        # type d'instruction : hexadécimale
        elif self.selected_typeInstruction.text()[:3] == "Hex":
            with open(resource_path("ConversionFiles\\Hexa.txt"), "w") as f:
                f.write(self.instruction)
            f.close()
            writeBinaryInstructions(resource_path("ConversionFiles\\Hexa.txt"), True)
            describe_instructions(self.selected_OptionConversion.text(), True)

        # type d'instruction : binaire
        elif self.selected_typeInstruction.text()[:3] == "Bin":
            with open(resource_path("ConversionFiles\\instructions_file.txt"), "w") as f:
                f.write(self.instruction)
            f.close()
            describe_instructions(self.selected_OptionConversion.text(), True)

        with open(resource_path("ConversionFiles\\Assembly.txt"), "r") as f:
            assembly_code = f.read()
        f.close()
        self.ConvertedInstructionText.setText(assembly_code)

    def setupUi(self):
        # définition des polices d'écriture utilisées
        font1 = QtGui.QFont()
        font1.setPointSize(14)
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        font3 = QtGui.QFont()
        font3.setPointSize(10)
        font4 = QtGui.QFont()
        font4.setPointSize(11)
        font5 = QtGui.QFont()
        font5.setPointSize(18)

        # paramètres généraux de la fenêtre
        self.setWindowTitle(self.JSON_lang["SC_Title"])
        self.resize(835, 544)
        self.setFixedSize(835, 544)
        icon = QIcon(resource_path("graphicResources/ApplicationIcon.ico"))
        self.setWindowIcon(icon)

        # Layout global
        self.GlobalLayout = QVBoxLayout(self)
        self.GlobalLayout.setObjectName("GlobalLayout")

        # layout du titre
        self.TitleLayout = QtWidgets.QHBoxLayout()
        self.TitleLayout.setObjectName("TitleLayout")

        # spacer à gauche du titre
        LeftTitleSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.TitleLayout.addItem(LeftTitleSpacer)

        # titre de la fenêtre
        self.Title = QtWidgets.QLabel()
        self.Title.setFont(font1)
        self.Title.setObjectName("Title")
        self.TitleLayout.addWidget(self.Title)

        # spacer à droite du titre
        RightTitleSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.TitleLayout.addItem(RightTitleSpacer)
        self.GlobalLayout.addLayout(self.TitleLayout)

        # spacer sous le titre
        TitleToOptionsSpacer = QtWidgets.QSpacerItem(13, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(TitleToOptionsSpacer)

        # layout global des options
        self.GlobalOptionsLayout = QtWidgets.QHBoxLayout()
        self.GlobalOptionsLayout.setObjectName("GlobalOptionsLayout")

        # spacer à gauche des options
        LeftInstructionOptionsSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.GlobalOptionsLayout.addItem(LeftInstructionOptionsSpacer)

        # layout des types d'instructions
        self.InstructionOptionsLayout = QtWidgets.QVBoxLayout()
        self.InstructionOptionsLayout.setObjectName("InstructionOptionsLayout")

        # titre des types d'instructions
        self.InstructionTypeTitle = QtWidgets.QLabel()
        self.InstructionTypeTitle.setFont(font2)
        self.InstructionTypeTitle.setObjectName("InstructionTypeTittle")
        self.InstructionOptionsLayout.addWidget(self.InstructionTypeTitle)

        # option type hexadécimal
        self.TypeInstruction_Group = QButtonGroup()
        self.HexadecimalInstruction = QtWidgets.QRadioButton()
        self.HexadecimalInstruction.setFont(font3)
        self.HexadecimalInstruction.setObjectName("HexadecimalInstruction")
        self.TypeInstruction_Group.addButton(self.HexadecimalInstruction)
        self.InstructionOptionsLayout.addWidget(self.HexadecimalInstruction)

        # option type binaire
        self.BinaryInstruction = QtWidgets.QRadioButton()
        self.BinaryInstruction.setFont(font3)
        self.BinaryInstruction.setObjectName("BinaryInstruction")
        self.TypeInstruction_Group.addButton(self.BinaryInstruction)
        self.InstructionOptionsLayout.addWidget(self.BinaryInstruction)
        self.GlobalOptionsLayout.addLayout(self.InstructionOptionsLayout)

        # spacer entre les 2 parties des options
        BetweenOptionsSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.GlobalOptionsLayout.addItem(BetweenOptionsSpacer)

        # layout des options de conversion
        self.ConversionOptionsLayout = QtWidgets.QVBoxLayout()
        self.ConversionOptionsLayout.setObjectName("ConversionOptionsLayout")

        # titre des options de conversion
        self.ConversionOptionsTitle = QtWidgets.QLabel()
        self.ConversionOptionsTitle.setFont(font2)
        self.ConversionOptionsTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.ConversionOptionsTitle.setObjectName("ConversionOptionsTittle")
        self.ConversionOptionsLayout.addWidget(self.ConversionOptionsTitle)

        # option conversion "Compact"
        self.ConversionOption_Group = QButtonGroup()
        self.CompactOption = QtWidgets.QRadioButton()
        self.CompactOption.setFont(font3)
        self.CompactOption.setObjectName("CompactOption")
        self.CompactOption.setChecked(True)
        self.ConversionOption_Group.addButton(self.CompactOption)
        self.ConversionOptionsLayout.addWidget(self.CompactOption)

        # option conversion "Classique"
        self.ClassiqueOption = QtWidgets.QRadioButton()
        self.ClassiqueOption.setFont(font3)
        self.ClassiqueOption.setObjectName("ClassiqueOption")
        self.ConversionOption_Group.addButton(self.ClassiqueOption)
        self.ConversionOptionsLayout.addWidget(self.ClassiqueOption)

        # option conversion "Intégrale"
        self.IntegralOption = QtWidgets.QRadioButton()
        self.IntegralOption.setFont(font3)
        self.IntegralOption.setObjectName("IntegralOption")
        self.ConversionOption_Group.addButton(self.IntegralOption)
        self.ConversionOptionsLayout.addWidget(self.IntegralOption)
        self.GlobalOptionsLayout.addLayout(self.ConversionOptionsLayout)

        # spacer droite des options
        RightOptionsSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.GlobalOptionsLayout.addItem(RightOptionsSpacer)
        self.GlobalLayout.addLayout(self.GlobalOptionsLayout)

        # spacer sous options
        OptionsToInsertInstructionsSpacer = QtWidgets.QSpacerItem(17, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(OptionsToInsertInstructionsSpacer)

        # layout insertion instruction
        self.InsertInstructionLayout = QtWidgets.QHBoxLayout()
        self.InsertInstructionLayout.setObjectName("InsertInstructionLayout")

        # spacer gauche titre insertion instruction
        LeftInsertInstructionSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.InsertInstructionLayout.addItem(LeftInsertInstructionSpacer)

        # titre insertion instruction
        self.InsertInstructionTittle = QtWidgets.QLabel()
        self.InsertInstructionTittle.setFont(font4)
        self.InsertInstructionTittle.setObjectName("InsertInstructionTittle")
        self.InsertInstructionLayout.addWidget(self.InsertInstructionTittle)

        # spacer droite titre insertion instruction
        RightInsertInstructionSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.InsertInstructionLayout.addItem(RightInsertInstructionSpacer)
        self.GlobalLayout.addLayout(self.InsertInstructionLayout)

        # zone de texte insertion instruction
        self.RawInstructionText = QtWidgets.QTextEdit()
        self.RawInstructionText.setMaximumSize(QtCore.QSize(16777215, 50))
        self.RawInstructionText.setFont(font2)
        self.RawInstructionText.setObjectName("RawInstructionText")
        self.GlobalLayout.addWidget(self.RawInstructionText)

        # spacer sous zone de texte insertion instruction
        RawInstructionToConvertButtonSpacer = QtWidgets.QSpacerItem(17, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(RawInstructionToConvertButtonSpacer)

        # layout bouton conversion
        self.ConvertButtonLayout = QtWidgets.QHBoxLayout()
        self.ConvertButtonLayout.setObjectName("ConvertButtonLayout")

        # spacer gauche bouton conversion
        LeftConvertButtonSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ConvertButtonLayout.addItem(LeftConvertButtonSpacer)

        # bouton conversion
        self.ConvertButton = QtWidgets.QPushButton()
        self.ConvertButton.setFont(font5)
        self.ConvertButton.setObjectName("ConvertButton")
        self.ConvertButtonLayout.addWidget(self.ConvertButton)

        # spacer droite bouton conversion
        RightConvertButtonSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ConvertButtonLayout.addItem(RightConvertButtonSpacer)
        self.GlobalLayout.addLayout(self.ConvertButtonLayout)

        # spacer sous bouton conversion
        ConvertButtonToResultTitleSpacer = QtWidgets.QSpacerItem(17, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(ConvertButtonToResultTitleSpacer)

        # layout résultat conversion
        self.ResultConversionLayout = QtWidgets.QHBoxLayout()
        self.ResultConversionLayout.setObjectName("ResultConversionLayout")

        # spacer gauche titre résultat conversion
        LeftResultTitleSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultConversionLayout.addItem(LeftResultTitleSpacer)

        # titre résultat conversion
        self.ResultTitle = QtWidgets.QLabel()
        self.ResultTitle.setFont(font4)
        self.ResultTitle.setObjectName("ResultTittle")
        self.ResultConversionLayout.addWidget(self.ResultTitle)

        # spacer droite titre résultat conversion
        RightResultTitleSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultConversionLayout.addItem(RightResultTitleSpacer)
        self.GlobalLayout.addLayout(self.ResultConversionLayout)

        # zone de texte résultat conversion
        self.ConvertedInstructionText = QtWidgets.QTextEdit()
        self.ConvertedInstructionText.setMaximumSize(QtCore.QSize(16777215, 60))
        self.ConvertedInstructionText.setFont(font2)
        self.ConvertedInstructionText.setObjectName("ConvertedInstructionText")
        self.ConvertedInstructionText.setReadOnly(True)
        self.GlobalLayout.addWidget(self.ConvertedInstructionText)

        # spacer sous zone de texte résultat conversion
        ConvertedInstructionToBottomSpacer = QtWidgets.QSpacerItem(18, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(ConvertedInstructionToBottomSpacer)

        # Partie connection aux actions quand clic de l'utilisateur
        self.TypeInstruction_Group.buttonClicked.connect(self.store_TypeInstruction)
        self.ConversionOption_Group.buttonClicked.connect(self.store_OptionConversion)
        self.ConvertButton.clicked.connect(self.translate)

        # initialisation des noms des objets et connexion aux slots
        self.NameInit()
        QtCore.QMetaObject.connectSlotsByName(self)
