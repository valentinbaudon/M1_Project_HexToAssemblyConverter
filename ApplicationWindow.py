from PyQt5.QtWidgets import QFileDialog, QButtonGroup
import os
from conversionHexToAssembly import *
from SecondaryWindows import *


class MainWindow(object):
    # Constructeur de la classe
    def __init__(self):
        # Initialisation des attributs de la classe
        self.actionFrancais = None
        self.actionEnglish = None
        self.menuLangues = None
        self.selected_hex_file = None
        self.NewWindow = None
        self.actionQuitter = None
        self.menuFichier = None
        self.menuFonctionnement = None
        self.actionClearFiles = None
        self.actionNouvellefenetre = None
        self.radioValue = None
        self.checked_button = None
        self.button_group = None
        self.explanation = None
        self.about = None
        self.menu_Help = None
        self.menubar = None
        self.DownloadAssemblyButton = None
        self.statusbar = None
        self.DownloadAssemblyButtonLayout = None
        self.actionAbout = None
        self.actionFonctionnement = None
        self.HowToDownloadAssembly_Text = None
        self.line_HautFooter = None
        self.line_5 = None
        self.line_RightCenter = None
        self.convertButton = None
        self.FooterLayout = None
        self.ConvertButtonLayout = None
        self.Exemple_OptionConversion = None
        self.radioButton_3 = None
        self.radioButton_2 = None
        self.radioButton_1 = None
        self.OptionsLayout = None
        self.OptionsGlobalLayout = None
        self.optionConversion_Title = None
        self.DownloadHexButton = None
        self.DownloadHexButtonLayout = None
        self.HowToDownloadHex_Text = None
        self.DownloadHexLayout = None
        self.OptionsConversionLayout = None
        self.line_TextOptions = None
        self.AssemblyCode = None
        self.Assembly_Code_Title = None
        self.HexaCode = None
        self.Hex_Code_Title = None
        self.TextCodesLayout = None
        self.TextCodesGlobalLayout = None
        self.line_LeftText = None
        self.CentralLayout = None
        self.line_TitleCentral = None
        self.Title = None
        self.GlobalLayout = None
        self.centralwidget = None

        # Initialisation de l'option d'affichage sélectionnée par défaut
        self.selected_button = QtWidgets.QRadioButton()
        self.selected_button.setText("Compact")

        # Reset des fichiers hexa et assembleur
        with open("./ConversionFiles/Hexa.txt", "w") as f:
            f.write("")
        with open("./ConversionFiles/Assembly.txt", "w") as f:
            f.write("")

        # Gestion de la langue d'affichage par défaut comme étant la même que celle du système de l'utilisateur
        if locale.getlocale()[0] in ["fr_FR", "en_EN"]:
            self.JSON_lang = json.load(open("./OtherFiles/text_" + locale.getlocale()[0] + ".json"))
        else:
            self.JSON_lang = json.load(open("./OtherFiles/text_en_EN.json"))

    # Fonction permettant d'ouvrir la fenêtre "Fonctionnement"
    def ExplanationWindow(self):
        self.explanation = Functionning()
        showFunctioningWindow()

    # Fonction permettant d'ouvrir la fenêtre "À propos"
    def AboutWindow(self):
        self.about = About()
        showAboutWindow()

    # Fonction qui efface les fichiers
    def clearAllFiles(self):
        with open("./ConversionFiles/Hexa.txt", "w") as f:
            f.write("")
        with open("./ConversionFiles/Assembly.txt", "w") as f:
            f.write("")

        with open("./ConversionFiles/Hexa.txt", "r") as f:
            hexa = f.read()
        self.HexaCode.setText(hexa)
        with open("./ConversionFiles/Assembly.txt", "r") as f:
            assembly = f.read()
        self.AssemblyCode.setText(assembly)

        with open("./ConversionFiles/instructions_file.txt", "w") as f:
            f.write("")

    # Fonction permettant de faire la traduction du fichier hexa et de mettre le résultat dans le fichier "Assembly.txt"
    def translate(self):
        writeBinaryInstructions("./ConversionFiles/Hexa.txt")
        describe_instructions(self.selected_button.text())

        with open("./ConversionFiles/Assembly.txt", "r") as f:
            assembly_code = f.read()
        self.AssemblyCode.setText(assembly_code)

    # fonction permettant de télécharger le contenu d"un fichier hexa présent sur notre ordi qui sera mis dans le fichier "Hexa.txt" pour être traîté
    def download_hex_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier .srec", "",
                                                   "Fichiers .srec (*.srec);;Tous les fichiers ()", options=options)
        if file_name:
            hex_name = os.path.basename(file_name).rpartition(".")[0]
            newHexName = hex_name + "_assembly.txt"
            self.selected_hex_file = newHexName
            with open(file_name, "r") as f:
                hexa_code = f.read()
            with open("./ConversionFiles/Hexa.txt", "w") as f1:
                f1.write(hexa_code)
            self.HexaCode.setText(hexa_code)

    # Fonction permettant de télécharger sur notre ordi le fichier converti
    def download_assembly_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(None, "Enregistrer le fichier Assembly.txt", self.selected_hex_file,
                                                   "Fichiers texte (.txt);;Tous les fichiers ()", options=options)
        if file_name:
            with open("./ConversionFiles/Assembly.txt", "r") as f:
                assembly_code = f.read()
            with open(file_name, "w") as f:
                f.write(assembly_code)

    # Fonction permettant de mettre à jour le boutton d'option d'affichage sélectionnée
    def store_selection(self, button):
        self.selected_button = button

    # Fonction permettant de changer la langue d'affichage en français
    def select_language_fr(self):
        self.JSON_lang = json.load(open("./OtherFiles/text_fr_FR.json"))
        self.NameInit()

    # Fonction permettant de changer la langue d'affichage en anglais
    def select_language_en(self):
        self.JSON_lang = json.load(open("./OtherFiles/text_en_EN.json"))
        self.NameInit()

    # Partie initialisation des textes et noms des éléments de la fenêtre
    def NameInit(self):
        _translate = QtCore.QCoreApplication.translate
        self.Title.setText(_translate("Converter", self.JSON_lang["Title"]))
        self.Hex_Code_Title.setText(_translate("Converter", self.JSON_lang["Hex_Code_Title"]))
        self.Assembly_Code_Title.setText(_translate("Converter", self.JSON_lang["Assembly_Code_Title"]))
        self.HowToDownloadHex_Text.setText(_translate("Converter", self.JSON_lang["HowToDownloadHex_Text"]))
        self.DownloadHexButton.setText(_translate("Converter", self.JSON_lang["DownloadHexButton"]))
        self.optionConversion_Title.setText(_translate("Converter", self.JSON_lang["optionConversion_Title"]))
        self.radioButton_1.setText(_translate("Converter", self.JSON_lang["radioButton_1"]))
        self.radioButton_2.setText(_translate("Converter", self.JSON_lang["radioButton_2"]))
        self.radioButton_3.setText(_translate("Converter", self.JSON_lang["radioButton_3"]))
        self.Exemple_OptionConversion.setText(_translate("Converter", self.JSON_lang["Exemple_OptionConversion"]))
        self.convertButton.setText(_translate("Converter", self.JSON_lang["convertButton"]))
        self.HowToDownloadAssembly_Text.setText(_translate("Converter", self.JSON_lang["HowToDownloadAssembly_Text"]))
        self.DownloadAssemblyButton.setText(_translate("Converter", self.JSON_lang["DownloadAssemblyButton"]))
        self.menu_Help.setTitle(_translate("Converter", self.JSON_lang["menu_Help"]))
        self.menuFonctionnement.setTitle(_translate("Converter", self.JSON_lang["menuFonctionnement"]))
        self.menuFichier.setTitle(_translate("Converter", self.JSON_lang["menuFichier"]))
        self.menuLangues.setTitle(_translate("Converter", self.JSON_lang["menuLangues"]))
        self.actionAbout.setText(_translate("Converter", self.JSON_lang["actionAbout"]))
        self.actionFonctionnement.setText(_translate("Converter", self.JSON_lang["actionFonctionnement"]))
        self.actionClearFiles.setText(_translate("Converter", self.JSON_lang["actionClearFiles"]))
        self.actionQuitter.setText(_translate("Converter", self.JSON_lang["actionQuitter"]))
        self.actionFrancais.setText(_translate("Converter", self.JSON_lang["actionFrancais"]))
        self.actionEnglish.setText(_translate("Converter", self.JSON_lang["actionEnglish"]))

    # Fonction de définition des composants de notre fenêtre principale
    def setupUi(self, ConverterWindow):
        # paramètres généraux de la fenêtre
        ConverterWindow.setObjectName("HexaToAssemblyConverter")
        ConverterWindow.resize(1216, 842)
        ConverterWindow.setWindowState(QtCore.Qt.WindowMaximized)
        icon = QIcon("./OtherFiles/TemporaryIcon.ico")
        ConverterWindow.setWindowIcon(icon)

        # Paramètres de polices utilisées
        font = QtGui.QFont()
        font.setPointSize(15)
        font2 = QtGui.QFont()
        font2.setPointSize(9)
        font3 = QtGui.QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setWeight(50)
        font4 = QtGui.QFont()
        font4.setPointSize(12)
        font5 = QtGui.QFont()
        font5.setPointSize(25)

        # Objet central
        self.centralwidget = QtWidgets.QWidget(ConverterWindow)
        self.centralwidget.setObjectName("centralwidget")
        ConverterWindow.setCentralWidget(self.centralwidget)

        # Layout global
        self.GlobalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.GlobalLayout.setObjectName("GlobalLayout")

        # Titre de la page
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setFont(font)
        self.Title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.Title.setObjectName("Title")
        self.GlobalLayout.addWidget(self.Title)

        # Spacer entre le titre et la partie centrale
        spacerItem = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.GlobalLayout.addItem(spacerItem)

        # Ligne entre le titre et la partie centrale
        self.line_TitleCentral = QtWidgets.QFrame(self.centralwidget)
        self.line_TitleCentral.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_TitleCentral.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_TitleCentral.setObjectName("line_TitleCentral")
        self.GlobalLayout.addWidget(self.line_TitleCentral)

        # Layout de la partie centrale
        self.CentralLayout = QtWidgets.QHBoxLayout()
        self.CentralLayout.setObjectName("CentralLayout")

        # Ligne à gauche de la partie texte
        self.line_LeftText = QtWidgets.QFrame(self.centralwidget)
        self.line_LeftText.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_LeftText.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_LeftText.setObjectName("line_LeftText")
        self.CentralLayout.addWidget(self.line_LeftText)

        # Layout global de la partie d'affichage des codes
        self.TextCodesGlobalLayout = QtWidgets.QWidget(self.centralwidget)
        self.TextCodesGlobalLayout.setObjectName("TextCodesGlobalLayout")

        # Layout de la partie d'affichage des codes
        self.TextCodesLayout = QtWidgets.QVBoxLayout(self.TextCodesGlobalLayout)
        self.TextCodesLayout.setObjectName("TextCodesLayout")

        # Objet titre du texte en hexadecimal
        self.Hex_Code_Title = QtWidgets.QLabel(self.TextCodesGlobalLayout)
        self.Hex_Code_Title.setFont(font)
        self.Hex_Code_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Hex_Code_Title.setObjectName("Hex_Code_Title")
        self.TextCodesLayout.addWidget(self.Hex_Code_Title)

        # Objet texte en hexadecimal
        self.HexaCode = QtWidgets.QTextEdit(self.TextCodesGlobalLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HexaCode.sizePolicy().hasHeightForWidth())
        self.HexaCode.setSizePolicy(sizePolicy)
        self.HexaCode.setMaximumSize(QtCore.QSize(16777215, 400))
        self.HexaCode.setObjectName("HexaCode")
        self.TextCodesLayout.addWidget(self.HexaCode)

        # Objet titre du texte en assembleur
        self.Assembly_Code_Title = QtWidgets.QLabel(self.TextCodesGlobalLayout)
        self.Assembly_Code_Title.setFont(font)
        self.Assembly_Code_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Assembly_Code_Title.setObjectName("Assembly_Code_Title")
        self.TextCodesLayout.addWidget(self.Assembly_Code_Title)

        # Objet texte en assembleur
        self.AssemblyCode = QtWidgets.QTextEdit(self.TextCodesGlobalLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AssemblyCode.sizePolicy().hasHeightForWidth())
        self.AssemblyCode.setSizePolicy(sizePolicy)
        self.AssemblyCode.setMinimumSize(QtCore.QSize(300, 400))
        self.AssemblyCode.setObjectName("AssemblyCode")
        self.AssemblyCode.setFont(font4)
        self.AssemblyCode.setReadOnly(True)
        self.TextCodesLayout.addWidget(self.AssemblyCode)
        self.CentralLayout.addWidget(self.TextCodesGlobalLayout)

        # Ligne entre la partie texte et la partie options et conversion
        self.line_TextOptions = QtWidgets.QFrame(self.centralwidget)
        self.line_TextOptions.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_TextOptions.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_TextOptions.setObjectName("line_TextOptions")
        self.CentralLayout.addWidget(self.line_TextOptions)

        # Layout partie options et conversion
        self.OptionsConversionLayout = QtWidgets.QVBoxLayout()
        self.OptionsConversionLayout.setObjectName("OptionsConversionLayout")

        # Layout partie téléchargement fichier hexa
        self.DownloadHexLayout = QtWidgets.QVBoxLayout()
        self.DownloadHexLayout.setObjectName("DownloadHexLayout")

        # Spacer entre haut de partie centrale et layout partie téléchargement fichier hexa
        spacer_HighCentral_DownloadHexLayout = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Minimum,
                                                                     QtWidgets.QSizePolicy.Fixed)
        self.DownloadHexLayout.addItem(spacer_HighCentral_DownloadHexLayout)

        # Objet texte indication téléchargement hexa
        self.HowToDownloadHex_Text = QtWidgets.QLabel(self.centralwidget)
        self.HowToDownloadHex_Text.setFont(font)
        self.HowToDownloadHex_Text.setAlignment(QtCore.Qt.AlignCenter)
        self.HowToDownloadHex_Text.setObjectName("HowToDownloadHex_Text")
        self.DownloadHexLayout.addWidget(self.HowToDownloadHex_Text)

        # Layout autour du bouton de téléchargement du fichier hexa
        self.DownloadHexButtonLayout = QtWidgets.QHBoxLayout()
        self.DownloadHexButtonLayout.setObjectName("DownloadHexButtonLayout")

        # Spacer entre gauche partie conversion et bouton conversion
        spacer_LeftConversion_DownloadHexButton = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                                        QtWidgets.QSizePolicy.Minimum)
        self.DownloadHexButtonLayout.addItem(spacer_LeftConversion_DownloadHexButton)

        # Bouton de téléchargement du fichier hexa
        self.DownloadHexButton = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadHexButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.DownloadHexButton.setFont(font2)
        self.DownloadHexButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.DownloadHexButton.setObjectName("DownloadHexButton")
        self.DownloadHexButtonLayout.addWidget(self.DownloadHexButton)

        # Spacer entre droite partie conversion et bouton conversion
        spacer_RightConversion_DownloadHexButton = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                                         QtWidgets.QSizePolicy.Minimum)
        self.DownloadHexButtonLayout.addItem(spacer_RightConversion_DownloadHexButton)
        self.DownloadHexLayout.addLayout(self.DownloadHexButtonLayout)
        self.OptionsConversionLayout.addLayout(self.DownloadHexLayout)

        # Spacer entre téléchargement hexa et options d'affichage
        spacer_OptionAffichage_DownloadHexButton = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum,
                                                                         QtWidgets.QSizePolicy.Expanding)
        self.OptionsConversionLayout.addItem(spacer_OptionAffichage_DownloadHexButton)

        # Titre de la partie sélection d'options d'affichage
        self.optionConversion_Title = QtWidgets.QLabel(self.centralwidget)
        self.optionConversion_Title.setFont(font)
        self.optionConversion_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.optionConversion_Title.setObjectName("optionConversion_Title")
        self.OptionsConversionLayout.addWidget(self.optionConversion_Title)

        # Layout global partie options d'affichage
        self.OptionsGlobalLayout = QtWidgets.QHBoxLayout()
        self.OptionsGlobalLayout.setObjectName("OptionsGlobalLayout")

        # Spacer entre ???
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.OptionsGlobalLayout.addItem(spacerItem6)

        # Layout contenant les boutons d'options d'affichage
        self.OptionsLayout = QtWidgets.QVBoxLayout()
        self.OptionsLayout.setObjectName("OptionsLayout")
        self.button_group = QButtonGroup()

        # Bouton option d'affichage compact
        self.radioButton_1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_1.setFont(font)
        self.radioButton_1.setObjectName("radioButton_1")
        self.OptionsLayout.addWidget(self.radioButton_1)
        self.button_group.addButton(self.radioButton_1)
        self.radioButton_1.setChecked(True)

        # Bouton option d'affichage classique
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.OptionsLayout.addWidget(self.radioButton_2)
        self.button_group.addButton(self.radioButton_2)

        # Bouton option d'affichage intégral
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.OptionsLayout.addWidget(self.radioButton_3)
        self.button_group.addButton(self.radioButton_3)
        self.checked_button = self.button_group.checkedButton()
        self.OptionsGlobalLayout.addLayout(self.OptionsLayout)

        # Spacer entre droite partie conversion et options d'affichage
        spacer_RightConversion_OptionAffichage = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                                       QtWidgets.QSizePolicy.Minimum)
        self.OptionsGlobalLayout.addItem(spacer_RightConversion_OptionAffichage)
        self.OptionsConversionLayout.addLayout(self.OptionsGlobalLayout)

        # Spacer entre gauche partie conversion et options d'affichage
        spacer_LeftConversion_OptionAffichage = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                                      QtWidgets.QSizePolicy.Expanding)
        self.OptionsConversionLayout.addItem(spacer_LeftConversion_OptionAffichage)

        # Texte exemple options d'affichage
        self.Exemple_OptionConversion = QtWidgets.QLabel(self.centralwidget)
        self.Exemple_OptionConversion.setFont(font4)
        self.Exemple_OptionConversion.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Exemple_OptionConversion.setWordWrap(False)
        self.Exemple_OptionConversion.setObjectName("Exemple_OptionConversion")
        self.OptionsConversionLayout.addWidget(self.Exemple_OptionConversion)

        # Spacer entre haut bouton conversion et options d'affichage
        spacer_ConvertButton_OptionAffichage = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum,
                                                                     QtWidgets.QSizePolicy.Expanding)
        self.OptionsConversionLayout.addItem(spacer_ConvertButton_OptionAffichage)

        # Layout autour du bouton de conversion
        self.ConvertButtonLayout = QtWidgets.QHBoxLayout()
        self.ConvertButtonLayout.setObjectName("ConvertButtonLayout")

        # Spacer bas bouton conversion
        spacer_lowConvertButton = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                        QtWidgets.QSizePolicy.Minimum)
        self.ConvertButtonLayout.addItem(spacer_lowConvertButton)

        # Bouton de conversion
        self.convertButton = QtWidgets.QPushButton(self.centralwidget)
        self.convertButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.convertButton.setFont(font5)
        self.convertButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.convertButton.setObjectName("convertButton")
        self.ConvertButtonLayout.addWidget(self.convertButton)

        # Spacer droite bouton conversion
        spacer_RightConvertButton = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                          QtWidgets.QSizePolicy.Minimum)
        self.ConvertButtonLayout.addItem(spacer_RightConvertButton)
        self.OptionsConversionLayout.addLayout(self.ConvertButtonLayout)

        # Spacer gauche bouton conversion
        spacer_LeftConvertButton = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum,
                                                         QtWidgets.QSizePolicy.Expanding)
        self.OptionsConversionLayout.addItem(spacer_LeftConvertButton)
        self.CentralLayout.addLayout(self.OptionsConversionLayout)

        # Ligne à droite de l'application
        self.line_RightCenter = QtWidgets.QFrame(self.centralwidget)
        self.line_RightCenter.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_RightCenter.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_RightCenter.setObjectName("line_RightCenter")
        self.CentralLayout.addWidget(self.line_RightCenter)
        self.GlobalLayout.addLayout(self.CentralLayout)

        # Layout de la partie basse de l'application
        self.FooterLayout = QtWidgets.QVBoxLayout()
        self.FooterLayout.setObjectName("FooterLayout")

        # Ligne entre le footer et le reste de l'application
        self.line_HautFooter = QtWidgets.QFrame(self.centralwidget)
        self.line_HautFooter.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_HautFooter.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_HautFooter.setObjectName("line_HautFooter")
        self.FooterLayout.addWidget(self.line_HautFooter)

        # Spacer entre line_HautFooter et le footer
        spacer_HautFooter = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.FooterLayout.addItem(spacer_HautFooter)

        # Objet texte indication téléchargement assembleur
        self.HowToDownloadAssembly_Text = QtWidgets.QLabel(self.centralwidget)
        self.HowToDownloadAssembly_Text.setFont(font)
        self.HowToDownloadAssembly_Text.setAlignment(QtCore.Qt.AlignCenter)
        self.HowToDownloadAssembly_Text.setObjectName("HowToDownloadAssembly_Text")
        self.FooterLayout.addWidget(self.HowToDownloadAssembly_Text)

        # Layout autour du bouton de téléchargement de l'assembleur
        self.DownloadAssemblyButtonLayout = QtWidgets.QHBoxLayout()
        self.DownloadAssemblyButtonLayout.setObjectName("DownloadAssemblyButtonLayout")

        # Spacer gauche bouton DownloadAssembly
        spacer_leftDownloadAssembly = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding,
                                                            QtWidgets.QSizePolicy.Minimum)
        self.DownloadAssemblyButtonLayout.addItem(spacer_leftDownloadAssembly)

        # Bouton de téléchargement de l'assembleur
        self.DownloadAssemblyButton = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadAssemblyButton.setMaximumSize(QtCore.QSize(400, 16777215))
        self.DownloadAssemblyButton.setFont(font2)
        self.DownloadAssemblyButton.setObjectName("DownloadAssemblyButton")
        self.DownloadAssemblyButtonLayout.addWidget(self.DownloadAssemblyButton)

        # Spacer droite bouton DownloadAssembly
        spacer_RightDownloadAssembly = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding,
                                                             QtWidgets.QSizePolicy.Minimum)
        self.DownloadAssemblyButtonLayout.addItem(spacer_RightDownloadAssembly)
        self.FooterLayout.addLayout(self.DownloadAssemblyButtonLayout)
        self.GlobalLayout.addLayout(self.FooterLayout)

        # PARTIE BARRE DE MENU

        # Initialisation de la barre de menu
        self.menubar = QtWidgets.QMenuBar(ConverterWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1216, 26))
        self.menubar.setObjectName("menubar")

        # Initialisation des parties de la barre de menu
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuFonctionnement = QtWidgets.QMenu(self.menubar)
        self.menuFonctionnement.setObjectName("menuFonctionnement")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuLangues = QtWidgets.QMenu(self.menuFichier)
        self.menuLangues.setObjectName("menuLangues")
        ConverterWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ConverterWindow)
        self.statusbar.setObjectName("statusbar")
        ConverterWindow.setStatusBar(self.statusbar)

        # Création de l'action liée au menu "à propos"
        self.actionAbout = QtWidgets.QAction(ConverterWindow)
        self.actionAbout.setObjectName("actionAbout")

        # Création de l'action liée au menu "fonctionnement"
        self.actionFonctionnement = QtWidgets.QAction(ConverterWindow)
        self.actionFonctionnement.setObjectName("actionFonctionnement")

        # Création de l'action liée au sous menu "nettoyer les fichiers"
        self.actionClearFiles = QtWidgets.QAction(ConverterWindow)
        self.actionClearFiles.setObjectName("actionClearFiles")

        # Création de l'action liée au sous menu "quitter"
        self.actionQuitter = QtWidgets.QAction(ConverterWindow)
        self.actionQuitter.setObjectName("actionQuitter")

        # Création de l'action liée au sous sous-menu "changer la langue en français"
        self.actionFrancais = QtWidgets.QAction(ConverterWindow)
        self.actionFrancais.setObjectName("actionFrancais")

        # Création de l'action liée au sous sous-menu "changer la langue en anglais"
        self.actionEnglish = QtWidgets.QAction(ConverterWindow)
        self.actionEnglish.setObjectName("actionEnglish")

        # Liaison entre les actions crées et les menus et sous menus
        self.menu_Help.addAction(self.actionAbout)
        self.menuFonctionnement.addAction(self.actionFonctionnement)
        self.menuFichier.addAction(self.actionClearFiles)
        self.menuLangues.addAction(self.actionFrancais)
        self.menuLangues.addAction(self.actionEnglish)
        self.menuFichier.addAction(self.menuLangues.menuAction())
        self.menuFichier.addAction(self.actionQuitter)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuFonctionnement.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        # Partie connection aux actions quand clic
        self.button_group.buttonClicked.connect(self.store_selection)
        self.convertButton.clicked.connect(self.translate)
        self.DownloadHexButton.clicked.connect(self.download_hex_file)
        self.DownloadAssemblyButton.clicked.connect(self.download_assembly_file)
        self.actionFonctionnement.triggered.connect(self.ExplanationWindow)
        self.actionFrancais.triggered.connect(self.select_language_fr)
        self.actionEnglish.triggered.connect(self.select_language_en)
        self.actionAbout.triggered.connect(self.AboutWindow)
        self.actionClearFiles.triggered.connect(self.clearAllFiles)
        self.actionQuitter.triggered.connect(ConverterWindow.close)

        # Affichage du fichier "Hexa.txt" dans la partie correpondante
        with open("./ConversionFiles/Hexa.txt", "r") as f:
            hexa_code = f.read()
        self.HexaCode.setText(hexa_code)

        # Initialisation des noms des objets de la fenêtre
        self.NameInit()
        _translate = QtCore.QCoreApplication.translate
        ConverterWindow.setWindowTitle(_translate("Converter", "Hexadecimal to Assembly Instructions Converter"))

        # Connexion de l'objet créé et de la fenêtre
        QtCore.QMetaObject.connectSlotsByName(ConverterWindow)
