from PyQt5.QtWidgets import QFileDialog, QButtonGroup
import os
from conversionHexToAssembly import *
from SecondaryWindows import *

test test
class MainWindow(object):
    # Constructeur de la classe
    def __init__(self):
        # initialisation des attributs de la classe
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
        self.selected_button = QtWidgets.QRadioButton()
        self.selected_button.setText("Compact")
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
        self.label_5 = None
        self.line_2 = None
        self.line_5 = None
        self.line_6 = None
        self.convertButton = None
        self.FooterLayout = None
        self.ConvertButtonLayout = None
        self.label_6 = None
        self.radioButton_3 = None
        self.radioButton_2 = None
        self.radioButton_1 = None
        self.OptionsLayout = None
        self.OptionsGlobalLayout = None
        self.label = None
        self.DownloadHexButton = None
        self.DownloadHexButtonLayout = None
        self.label_4 = None
        self.DownloadHexLayout = None
        self.verticalLayout = None
        self.line = None
        self.AssemblyCode = None
        self.label_3 = None
        self.HexaCode = None
        self.label_2 = None
        self.TextCodesLayout = None
        self.TextCodesGlobalLayout = None
        self.line_3 = None
        self.horizontalLayout = None
        self.line_4 = None
        self.Title = None
        self.verticalLayout_2 = None
        self.centralwidget = None

        # reset des fichiers hexa et assembleur
        with open("./ConversionFiles/Hexa.txt", "w") as f:
            f.write("")
        with open("./ConversionFiles/Assembly.txt", "w") as f:
            f.write("")

        if locale.getlocale()[0] in ["fr_FR", "en_EN"]:
            self.JSON_lang = json.load(open("./OtherFiles/text_" + locale.getlocale()[0] + ".json"))
        else:
            self.JSON_lang = json.load(open("./OtherFiles/text_en_EN.json"))

    # fonction permettant d'ouvrir la fenêtre "Fonctionnement"
    def ExplanationWindow(self):
        self.explanation = Functionning()
        showFunctioningWindow()

    # fonction permettant d'ouvrir la fenêtre "À propos"
    def AboutWindow(self):
        self.about = About()
        showAboutWindow()

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

    # fonction permettant de faire la traduction du fichier hexa et de mettre le résultat dans le fichier "Assembly.txt"
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

    # fonction permettant de télécharger sur notre ordi le fichier converti
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

    def store_selection(self, button):
        self.selected_button = button

    def select_language_fr(self):
        self.JSON_lang = json.load(open("./OtherFiles/text_fr_FR.json"))
        self.NameInit()

    def select_language_en(self):
        self.JSON_lang = json.load(open("./OtherFiles/text_en_EN.json"))
        self.NameInit()

    # partie initialisation des textes et noms des éléments de la fenêtre
    def NameInit(self):
        _translate = QtCore.QCoreApplication.translate
        self.Title.setText(_translate("Converter", self.JSON_lang["Title"]))
        self.label_2.setText(_translate("Converter", self.JSON_lang["label_2"]))
        self.label_3.setText(_translate("Converter", self.JSON_lang["label_3"]))
        self.label_4.setText(_translate("Converter", self.JSON_lang["label_4"]))
        self.DownloadHexButton.setText(_translate("Converter", self.JSON_lang["DownloadHexButton"]))
        self.label.setText(_translate("Converter", self.JSON_lang["label"]))
        self.radioButton_1.setText(_translate("Converter", self.JSON_lang["radioButton_1"]))
        self.radioButton_2.setText(_translate("Converter", self.JSON_lang["radioButton_2"]))
        self.radioButton_3.setText(_translate("Converter", self.JSON_lang["radioButton_3"]))
        self.label_6.setText(_translate("Converter", self.JSON_lang["label_6"]))
        self.convertButton.setText(_translate("Converter", self.JSON_lang["convertButton"]))
        self.label_5.setText(_translate("Converter", self.JSON_lang["label_5"]))
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

    # fonction de définition des composants de notre fenêtre principale
    def setupUi(self, ConverterWindow):
        # paramètres généraux de la fenêtre
        ConverterWindow.setObjectName("HexaToAssemblyConverter")
        ConverterWindow.resize(1216, 842)
        ConverterWindow.setWindowState(QtCore.Qt.WindowMaximized)
        icon = QIcon("./OtherFiles/TemporaryIcon.ico")
        ConverterWindow.setWindowIcon(icon)

        font = QtGui.QFont()
        font.setPointSize(15)
        font3 = QtGui.QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setWeight(50)
        font2 = QtGui.QFont()
        font2.setPointSize(9)
        font4 = QtGui.QFont()
        font4.setPointSize(12)

        # objet central
        self.centralwidget = QtWidgets.QWidget(ConverterWindow)
        self.centralwidget.setObjectName("centralwidget")
        ConverterWindow.setCentralWidget(self.centralwidget)

        # layout vertical 1
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Title = QtWidgets.QLabel(self.centralwidget)

        # titre de la page
        self.Title.setFont(font)
        self.Title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.Title.setObjectName("Title")
        self.verticalLayout_2.addWidget(self.Title)

        # spacer 1 : entre le titre et la partie centrale
        spacerItem = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)

        # ligne 1
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_2.addWidget(self.line_4)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)

        self.TextCodesGlobalLayout = QtWidgets.QWidget(self.centralwidget)
        self.TextCodesGlobalLayout.setObjectName("TextCodesGlobalLayout")

        self.TextCodesLayout = QtWidgets.QVBoxLayout(self.TextCodesGlobalLayout)
        self.TextCodesLayout.setObjectName("TextCodesLayout")

        self.label_2 = QtWidgets.QLabel(self.TextCodesGlobalLayout)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.TextCodesLayout.addWidget(self.label_2)

        self.HexaCode = QtWidgets.QTextEdit(self.TextCodesGlobalLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HexaCode.sizePolicy().hasHeightForWidth())
        self.HexaCode.setSizePolicy(sizePolicy)
        self.HexaCode.setMaximumSize(QtCore.QSize(16777215, 400))
        self.HexaCode.setObjectName("HexaCode")
        self.TextCodesLayout.addWidget(self.HexaCode)

        self.label_3 = QtWidgets.QLabel(self.TextCodesGlobalLayout)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.TextCodesLayout.addWidget(self.label_3)

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

        self.horizontalLayout.addWidget(self.TextCodesGlobalLayout)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.DownloadHexLayout = QtWidgets.QVBoxLayout()
        self.DownloadHexLayout.setObjectName("DownloadHexLayout")

        spacerItem2 = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.DownloadHexLayout.addItem(spacerItem2)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.DownloadHexLayout.addWidget(self.label_4)

        self.DownloadHexButtonLayout = QtWidgets.QHBoxLayout()
        self.DownloadHexButtonLayout.setObjectName("DownloadHexButtonLayout")

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.DownloadHexButtonLayout.addItem(spacerItem3)

        self.DownloadHexButton = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadHexButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.DownloadHexButton.setFont(font2)
        self.DownloadHexButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.DownloadHexButton.setObjectName("DownloadHexButton")
        self.DownloadHexButtonLayout.addWidget(self.DownloadHexButton)

        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.DownloadHexButtonLayout.addItem(spacerItem4)

        self.DownloadHexLayout.addLayout(self.DownloadHexButtonLayout)
        self.verticalLayout.addLayout(self.DownloadHexLayout)

        spacerItem5 = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.OptionsGlobalLayout = QtWidgets.QHBoxLayout()
        self.OptionsGlobalLayout.setObjectName("OptionsGlobalLayout")

        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.OptionsGlobalLayout.addItem(spacerItem6)

        self.OptionsLayout = QtWidgets.QVBoxLayout()
        self.OptionsLayout.setObjectName("OptionsLayout")
        self.button_group = QButtonGroup()

        self.radioButton_1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_1.setFont(font)
        self.radioButton_1.setObjectName("radioButton_1")
        self.OptionsLayout.addWidget(self.radioButton_1)
        self.button_group.addButton(self.radioButton_1)
        self.radioButton_1.setChecked(True)

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.OptionsLayout.addWidget(self.radioButton_2)
        self.button_group.addButton(self.radioButton_2)

        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.OptionsLayout.addWidget(self.radioButton_3)
        self.button_group.addButton(self.radioButton_3)
        self.checked_button = self.button_group.checkedButton()

        self.OptionsGlobalLayout.addLayout(self.OptionsLayout)

        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.OptionsGlobalLayout.addItem(spacerItem7)

        self.verticalLayout.addLayout(self.OptionsGlobalLayout)

        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setFont(font4)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_6.setWordWrap(False)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)

        spacerItem9 = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem9)

        self.ConvertButtonLayout = QtWidgets.QHBoxLayout()
        self.ConvertButtonLayout.setObjectName("ConvertButtonLayout")

        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.ConvertButtonLayout.addItem(spacerItem10)
        self.convertButton = QtWidgets.QPushButton(self.centralwidget)
        self.convertButton.setMaximumSize(QtCore.QSize(200, 16777215))
        font4 = QtGui.QFont()
        font4.setPointSize(25)
        self.convertButton.setFont(font4)
        self.convertButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.convertButton.setObjectName("convertButton")
        self.ConvertButtonLayout.addWidget(self.convertButton)

        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ConvertButtonLayout.addItem(spacerItem11)

        self.verticalLayout.addLayout(self.ConvertButtonLayout)

        spacerItem12 = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem12)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout.addWidget(self.line_6)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.FooterLayout = QtWidgets.QVBoxLayout()
        self.FooterLayout.setObjectName("FooterLayout")

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.FooterLayout.addWidget(self.line_2)

        spacerItem13 = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.FooterLayout.addItem(spacerItem13)

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.FooterLayout.addWidget(self.label_5)

        self.DownloadAssemblyButtonLayout = QtWidgets.QHBoxLayout()
        self.DownloadAssemblyButtonLayout.setObjectName("DownloadAssemblyButtonLayout")

        spacerItem14 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.DownloadAssemblyButtonLayout.addItem(spacerItem14)

        self.DownloadAssemblyButton = QtWidgets.QPushButton(self.centralwidget)
        self.DownloadAssemblyButton.setMaximumSize(QtCore.QSize(400, 16777215))
        self.DownloadAssemblyButton.setFont(font2)
        self.DownloadAssemblyButton.setObjectName("DownloadAssemblyButton")
        self.DownloadAssemblyButtonLayout.addWidget(self.DownloadAssemblyButton)

        spacerItem15 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.DownloadAssemblyButtonLayout.addItem(spacerItem15)

        self.FooterLayout.addLayout(self.DownloadAssemblyButtonLayout)
        self.verticalLayout_2.addLayout(self.FooterLayout)

        self.menubar = QtWidgets.QMenuBar(ConverterWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1216, 26))
        self.menubar.setObjectName("menubar")

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

        self.actionAbout = QtWidgets.QAction(ConverterWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.actionFonctionnement = QtWidgets.QAction(ConverterWindow)
        self.actionFonctionnement.setObjectName("actionFonctionnement")

        self.actionClearFiles = QtWidgets.QAction(ConverterWindow)
        self.actionClearFiles.setObjectName("actionClearFiles")

        self.actionQuitter = QtWidgets.QAction(ConverterWindow)
        self.actionQuitter.setObjectName("actionQuitter")

        self.actionFrancais = QtWidgets.QAction(ConverterWindow)
        self.actionFrancais.setObjectName("actionFrancais")

        self.actionEnglish = QtWidgets.QAction(ConverterWindow)
        self.actionEnglish.setObjectName("actionEnglish")

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

        # affichage du fichier "Hexa.txt" dans la partie correpondante
        with open("./ConversionFiles/Hexa.txt", "r") as f:
            hexa_code = f.read()
        self.HexaCode.setText(hexa_code)

        # initialisation des noms des objets de la fenêtre
        self.NameInit()
        _translate = QtCore.QCoreApplication.translate
        ConverterWindow.setWindowTitle(_translate("Converter", "Hexadecimal to Assembly Instructions Converter"))

        QtCore.QMetaObject.connectSlotsByName(ConverterWindow)
