import json
import locale
import os
import sys
from PyQt5 import QtWidgets, QtCore, Qt, QtGui
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QMainWindow, QLabel, QMenu, QAction, QButtonGroup

from conversionHexToAssembly import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


Logo = resource_path("Logo.png")


# Classe définissant la fenêtre "Functionning"
class Functionning(QDialog):
    # constructeur de la classe "Functionning"
    def __init__(self, langue):
        # récupération des initialisations de la classe mère
        super().__init__()

        # paramètres généraux de la fenêtre
        self.setWindowTitle("Fonctionnement de l'application de traduction")
        self.resize(700, 520)
        self.setFixedSize(700, 520)
        icon = QIcon(resource_path("graphicResources\\TemporaryIcon.ico"))
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
            JSON_lang = json.load(open(resource_path("OtherFiles\\text_fr_FR.json")))
        else:
            JSON_lang = json.load(open(resource_path("OtherFiles\\text_en_EN.json")))
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
        self.resize(650, 520)
        self.setFixedSize(650, 520)
        icon = QIcon(resource_path("graphicResources\\TemporaryIcon.ico"))
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
            JSON_lang = json.load(open(resource_path("OtherFiles\\text_fr_FR.json")))
        else:
            JSON_lang = json.load(open(resource_path("OtherFiles\\text_en_EN.json")))
        self.text_edit.setPlainText(JSON_lang["about"])
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

        # Gestion de la langue d'affichage par défaut comme étant la même que celle du système de l'utilisateur
        self.instruction = None
        self.selected_OptionConversion = None
        self.selected_typeInstruction = None
        self.ConversionOption_Group = None
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
        self.language = langue
        self.JSON_lang = json.load(open(resource_path("OtherFiles\\text_" + self.language + ".json")))

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

    def store_TypeInstruction(self, button):
        self.selected_typeInstruction = button

    def store_OptionConversion(self, button):
        self.selected_OptionConversion = button

    def translate(self):
        self.instruction = self.RawInstructionText.toPlainText()
        if self.selected_typeInstruction.text()[:3] == "Hex":
            with open(resource_path("ConversionFiles\\Hexa.txt"), "w") as f:
                f.write(self.instruction)
            f.close()
            writeBinaryInstructions(resource_path("ConversionFiles\\Hexa.txt"), True)
            describe_instructions(self.selected_OptionConversion.text(), True)
        else:
            with open(resource_path("ConversionFiles\\instructions_file.txt"), "w") as f:
                f.write(self.instruction)
            f.close()
            describe_instructions(self.selected_OptionConversion.text(), True)

        with open(resource_path("ConversionFiles\\Assembly.txt"), "r") as f:
            assembly_code = f.read()
        f.close()
        self.ConvertedInstructionText.setText(assembly_code)

    def setupUi(self):
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
        icon = QIcon(resource_path("graphicResources\\TemporaryIcon.ico"))
        self.setWindowIcon(icon)

        self.GlobalLayout = QVBoxLayout(self)
        self.GlobalLayout.setObjectName("GlobalLayout")

        self.TitleLayout = QtWidgets.QHBoxLayout()
        self.TitleLayout.setObjectName("TitleLayout")

        LeftTittleSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.TitleLayout.addItem(LeftTittleSpacer)

        self.Title = QtWidgets.QLabel()
        self.Title.setFont(font1)
        self.Title.setObjectName("Title")
        self.TitleLayout.addWidget(self.Title)

        RightTitleSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.TitleLayout.addItem(RightTitleSpacer)

        self.GlobalLayout.addLayout(self.TitleLayout)

        TitleToOptionsSpacer = QtWidgets.QSpacerItem(13, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(TitleToOptionsSpacer)

        self.GlobalOptionsLayout = QtWidgets.QHBoxLayout()
        self.GlobalOptionsLayout.setObjectName("GlobalOptionsLayout")
        LeftInstructionOptionsSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.GlobalOptionsLayout.addItem(LeftInstructionOptionsSpacer)

        self.InstructionOptionsLayout = QtWidgets.QVBoxLayout()
        self.InstructionOptionsLayout.setObjectName("InstructionOptionsLayout")

        self.InstructionTypeTitle = QtWidgets.QLabel()
        self.InstructionTypeTitle.setFont(font2)
        self.InstructionTypeTitle.setObjectName("InstructionTypeTittle")
        self.InstructionOptionsLayout.addWidget(self.InstructionTypeTitle)

        self.TypeInstruction_Group = QButtonGroup()

        self.HexadecimalInstruction = QtWidgets.QRadioButton()
        self.HexadecimalInstruction.setFont(font3)
        self.HexadecimalInstruction.setObjectName("HexadecimalInstruction")
        self.TypeInstruction_Group.addButton(self.HexadecimalInstruction)
        self.InstructionOptionsLayout.addWidget(self.HexadecimalInstruction)

        self.BinaryInstruction = QtWidgets.QRadioButton()
        self.BinaryInstruction.setFont(font3)
        self.BinaryInstruction.setObjectName("BinaryInstruction")
        self.TypeInstruction_Group.addButton(self.BinaryInstruction)
        self.InstructionOptionsLayout.addWidget(self.BinaryInstruction)
        self.GlobalOptionsLayout.addLayout(self.InstructionOptionsLayout)

        BetweenOptionsSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.GlobalOptionsLayout.addItem(BetweenOptionsSpacer)

        self.ConversionOptionsLayout = QtWidgets.QVBoxLayout()
        self.ConversionOptionsLayout.setObjectName("ConversionOptionsLayout")

        self.ConversionOptionsTitle = QtWidgets.QLabel()
        self.ConversionOptionsTitle.setFont(font2)
        self.ConversionOptionsTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.ConversionOptionsTitle.setObjectName("ConversionOptionsTittle")
        self.ConversionOptionsLayout.addWidget(self.ConversionOptionsTitle)

        self.ConversionOption_Group = QButtonGroup()

        self.CompactOption = QtWidgets.QRadioButton()
        self.CompactOption.setFont(font3)
        self.CompactOption.setObjectName("CompactOption")
        self.ConversionOption_Group.addButton(self.CompactOption)
        self.ConversionOptionsLayout.addWidget(self.CompactOption)

        self.ClassiqueOption = QtWidgets.QRadioButton()
        self.ClassiqueOption.setFont(font3)
        self.ClassiqueOption.setObjectName("ClassiqueOption")
        self.ConversionOption_Group.addButton(self.ClassiqueOption)
        self.ConversionOptionsLayout.addWidget(self.ClassiqueOption)

        self.IntegralOption = QtWidgets.QRadioButton()
        self.IntegralOption.setFont(font3)
        self.IntegralOption.setObjectName("IntegralOption")
        self.ConversionOption_Group.addButton(self.IntegralOption)
        self.ConversionOptionsLayout.addWidget(self.IntegralOption)
        self.GlobalOptionsLayout.addLayout(self.ConversionOptionsLayout)

        RightOptionsSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.GlobalOptionsLayout.addItem(RightOptionsSpacer)
        self.GlobalLayout.addLayout(self.GlobalOptionsLayout)

        OptionsToInsertInstructionsSpacer = QtWidgets.QSpacerItem(17, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(OptionsToInsertInstructionsSpacer)

        self.InsertInstructionLayout = QtWidgets.QHBoxLayout()
        self.InsertInstructionLayout.setObjectName("InsertInstructionLayout")

        LeftInsertInstructionSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.InsertInstructionLayout.addItem(LeftInsertInstructionSpacer)

        self.InsertInstructionTittle = QtWidgets.QLabel()
        self.InsertInstructionTittle.setFont(font4)
        self.InsertInstructionTittle.setObjectName("InsertInstructionTittle")
        self.InsertInstructionLayout.addWidget(self.InsertInstructionTittle)

        RightInsertInstructionSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.InsertInstructionLayout.addItem(RightInsertInstructionSpacer)
        self.GlobalLayout.addLayout(self.InsertInstructionLayout)

        self.RawInstructionText = QtWidgets.QTextEdit()
        self.RawInstructionText.setMaximumSize(QtCore.QSize(16777215, 50))
        self.RawInstructionText.setFont(font2)
        self.RawInstructionText.setObjectName("RawInstructionText")
        self.GlobalLayout.addWidget(self.RawInstructionText)

        RawInstructionToConvertButtonSpacer = QtWidgets.QSpacerItem(17, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(RawInstructionToConvertButtonSpacer)

        self.ConvertButtonLayout = QtWidgets.QHBoxLayout()
        self.ConvertButtonLayout.setObjectName("ConvertButtonLayout")
        LeftConvertButtonSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ConvertButtonLayout.addItem(LeftConvertButtonSpacer)

        self.ConvertButton = QtWidgets.QPushButton()
        self.ConvertButton.setFont(font5)
        self.ConvertButton.setObjectName("ConvertButton")
        self.ConvertButtonLayout.addWidget(self.ConvertButton)

        RightConvertButtonSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ConvertButtonLayout.addItem(RightConvertButtonSpacer)
        self.GlobalLayout.addLayout(self.ConvertButtonLayout)

        ConvertButtonToResultTittleSpacer = QtWidgets.QSpacerItem(17, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(ConvertButtonToResultTittleSpacer)

        self.ResultConversionLayout = QtWidgets.QHBoxLayout()
        self.ResultConversionLayout.setObjectName("ResultConversionLayout")
        LeftResultTittleSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultConversionLayout.addItem(LeftResultTittleSpacer)

        self.ResultTitle = QtWidgets.QLabel()
        self.ResultTitle.setFont(font4)
        self.ResultTitle.setObjectName("ResultTittle")
        self.ResultConversionLayout.addWidget(self.ResultTitle)

        RightResultTittleSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultConversionLayout.addItem(RightResultTittleSpacer)
        self.GlobalLayout.addLayout(self.ResultConversionLayout)

        self.ConvertedInstructionText = QtWidgets.QTextEdit()
        self.ConvertedInstructionText.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ConvertedInstructionText.setFont(font2)
        self.ConvertedInstructionText.setObjectName("ConvertedInstructionText")
        self.ConvertedInstructionText.setReadOnly(True)
        self.GlobalLayout.addWidget(self.ConvertedInstructionText)

        ConvertedInstructionToBottomSpacer = QtWidgets.QSpacerItem(18, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.GlobalLayout.addItem(ConvertedInstructionToBottomSpacer)

        self.TypeInstruction_Group.buttonClicked.connect(self.store_TypeInstruction)
        self.ConversionOption_Group.buttonClicked.connect(self.store_OptionConversion)
        self.ConvertButton.clicked.connect(self.translate)

        self.NameInit()
        QtCore.QMetaObject.connectSlotsByName(self)
