from ApplicationWindow import *

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HexaToAssemblyConverter = QtWidgets.QMainWindow()
    window = MainWindow()
    window.setupUi(HexaToAssemblyConverter)
    HexaToAssemblyConverter.show()
    sys.exit(app.exec_())
