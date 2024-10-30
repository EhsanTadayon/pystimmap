from add_behavior_dialog_ui import AddBehavior_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtGui, QtWidgets

class AddBehavior_Dialog(AddBehavior_Dialog):
    def __init__(self):
        super().__init__()

    def setupUi(self,dialog):
        super().setupUi(dialog)
        self.dialog = dialog
        self.dialog.setWindowTitle("Behavior Input Dialog")
        self.behavior = ''
        self.behavior_component = None
        
    def add_behavior_slot(self):
        self.behavior = self.behavior_lineedit.text()
        self.behavior_component = self.behavior_specifics_lineedit.text()
        self.dialog.accept()
        
    def reject(self):
        self.dialog.reject()
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    dialog = QDialog()


    ui = AddBehavior()
    ui.setupUi(dialog)
    dialog.show()
    #MainWindow.move(50,50)
    sys.exit(app.exec_())
