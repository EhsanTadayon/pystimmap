import sys
sys.path.append("..")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject,Qt, QDate, QTime
from mainwindow_ui import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QApplication, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from add_behavior_dialog_main import AddBehavior_Dialog
import pandas as pd
from PandasMain import PandasMain
from datetime import datetime
from collections import defaultdict
import pickle
import copy
#from plotting_app import PlottingApp



import os
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'


class App(Ui_MainWindow):

    def __init__(self):
        super().__init__()

    def setupUi(self,MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.MainWindow.setWindowTitle("InMap")
        self._set_date_time()
        
        #data
        self.data = {}
        self.stim_table_initiated= 0
        
        #behaviors
        with open('behaviors_dict.pickle','rb') as f:
            self.data['behaviors_dict'] = pickle.load(f)
            self.data['behaviors_dict_db'] = copy.deepcopy(self.data['behaviors_dict'])
            
        #load behaviors to behavior combobox
        for bh in self.data['behaviors_dict'].keys():
            self.response_behavior_combobox.addItem(bh)
    
        
    def _set_date_time(self):
        today = datetime.today()
        current_date = QDate(today.year, today.month, today.day)
        self.dateEdit.setDate(current_date)
        
        current_time = datetime.now()
        current_qtime = QTime(current_time.hour, current_time.minute, current_time.second)
        self.timeEdit.setTime(current_qtime)
    
        
    def freesurfer_dir_browse_slot(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        if dialog.exec_():
            freesurfer_dir = dialog.selectedFiles()[0]
            # add to data dictionary
            self.data['freesurfer_dir'] = freesurfer_dir

        
    def contacts_file_browse_slot(self):
        dialog = QtWidgets.QFileDialog()
        if dialog.exec_():
            contacts_file_path = dialog.selectedFiles()[0]
            # add to data dictionary
            self.data['contacts_file'] = contacts_file_path
            try:
                df = pd.read_csv(contacts_file_path)
                df.columns = ['contact','x','y','z']
                self.data['contacts_df'] = df
                
                ### now populate contacts in the inputs:
                self.input1_combobox.addItems(df['contact'].to_list())
                self.input2_combobox.addItems(df['contact'].to_list())
            except: 
                raise
            
        
    def output_dir_browse_slot(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        if dialog.exec_():
            output_dir = dialog.selectedFiles()[0]
            self.data['output_dir'] = output_dir
        
        
    def stim_file_browse_slot(self):
        dialog = QtWidgets.QFileDialog()
        if dialog.exec_():
            stim_file_path = dialog.selectedFiles()[0]
            # add stim file
            self.data['stim_file_path'] = stim_file_path
            self.data['df'] = pd.read_csv(stim_file_path)
        
    def add_stim_slot(self):

        if self._stim_df_is_available():
            task = self.task_combobox.currentText()
            input1 = self.input1_combobox.currentText()
            input2 = self.input2_combobox.currentText()
            stim_intensity = self.intensity_line.text()
            duration = self.duration_line.text()
            seizure = self.seizure_combobox.currentText()
            after_discharge = 1 if self.after_discharge_radiobutton.isChecked() else 0
            #behavior = self.response_behavior_combobox.currentText()
            behavior_subtype = ';'.join(get_all_items_in_list(self.selected_behavior_listwidget)) if len(self.selected_behavior_listwidget)>0 else 'None'
            response_comment = self.comment_textbox.toPlainText() if len(self.comment_textbox.toPlainText())>0 else 'None'
            intervention_med = self.intervention_medications_combobox.currentText()
            intervention_med_dose = self.intervention_medications_lineedit.text() if len(self.intervention_medications_lineedit.text())>0 else 'None'
            
            
            # 
            if input1=='Choose:' or input2=='Choose:':
                show_warning_dialog('Both contacts should be provided!')
            
            else:
            
                now = datetime.now()
        
                new_row = {'Time':now,
                            'Task':task,
                            'Input 1': input1,
                            'Input 2': input2,
                            'Intensity (mA)':stim_intensity, 
                            'Pulse Width (ms)': duration, 
                            'AD': after_discharge,
                            'Seizure':seizure,
                            'Behavior Response':behavior_subtype,
                            'Response Comment':response_comment,
                            'Medication':intervention_med,
                            'Dosage (mg)':intervention_med_dose,
                            }
        
                self.data['df'] = self.data['df']._append(new_row, ignore_index=True)
                self.data['df'].to_csv(self.data['df_path'],index=False)
                self.update_stim_table()
                self._reset()
        
    def _initiate_stim_table(self):
        if not self.stim_table_initiated: 
            stim_table_widget = PandasMain(self.pandas_widget)
            stim_table_widget.setup_ui(self.data['df'])
            self.data['stim_table_widget'] = stim_table_widget
            self.stim_table_initiated = 1
        #df_dialog.exec_()
        
    def update_stim_table(self):
        self.data['stim_table_widget'].update_table(self.data['df'])
    
    
    def populate_behavior_subcategory_slot(self):
        
        #get selected behavior
        behavior = self.response_behavior_combobox.currentText()
        
        #clear list
        self.behavior_listwidget.clear()
    
    
        for item in self.data['behaviors_dict'][behavior]:
            self.behavior_listwidget.addItem(item)

                
    def add_selected_behavior_to_list_slot(self):
            selected_items = self.behavior_listwidget.selectedItems()
            if not selected_items:
                QMessageBox.information(self, "No Selection", "Please select an item to add.")
                return

            for item in selected_items:
                if not is_item_in_list(item.text(), self.selected_behavior_listwidget):
                    self.selected_behavior_listwidget.addItem(item.text())
        
    def remove_selected_behavior_from_list_slot(self):
        selected_items = self.selected_behavior_listwidget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No Selection", "Please select an item to remove.")
            return

        for item in selected_items:
            self.selected_behavior_listwidget.takeItem(self.selected_behavior_listwidget.row(item))
   
  
    
    def _reset(self):
        #self.response_behavior_combobox.setCurrentText('')
        #self.behavior_listwidget.clear()
        self.selected_behavior_listwidget.clear()
        self.after_discharge_radiobutton.setChecked(False)
        self.seizure_combobox.setCurrentText('')
        self.comment_textbox.setText('')
        
    
    def increase_intensity_slot(self):
        current_int = float(self.intensity_line.text())
        new_int = current_int + 0.5
        self.intensity_line.setText(str(new_int))
        
    def increase_duration_slot(self):
        current_dur = float(self.duration_line.text())
        new_dur = current_dur + 0.5
        self.duration_line.setText(str(new_dur))
        
    def increase_frequency_slot(self):
        current_freq = float(self.frequency_line.text())
        new_freq = current_freq + 10
        self.frequency_line.setText(str(new_freq))
        
    def decrease_intensity_slot(self):
        current_int = float(self.intensity_line.text())
        new_int = current_int - 0.5
        self.intensity_line.setText(str(new_int))
    
    def decrease_frequency_slot(self):
        current_freq = float(self.frequency_line.text())
        new_freq = current_freq - 10
        self.frequency_line.setText(str(new_freq))
        
    def decrease_duration_slot(self):
        current_dur = float(self.duration_line.text())
        new_dur = current_dur - 0.5
        self.duration_line.setText(str(new_dur))
        
    def show_contact1_info(self):
        pass
        
    def show_contact2_info(self):
        pass
        
    
    def remove_stim_rows_slot(self):
        self.data['stim_table_widget'].remove_rows()
        self.data['df'] = self.data['stim_table_widget'].get_dataframe()
        self.data['df'].to_csv(self.data['df_path'],index=False)
        
    def add_new_behavior_slot(self):
        dialog = QDialog()
        behavior_dialog = AddBehavior_Dialog()
        behavior_dialog.setupUi(dialog)
        dialog.exec_()
        add_to_db = True if behavior_dialog.add_behavior_to_database_radiobutton.isChecked() else False
        behavior = behavior_dialog.behavior
        behavior_component = behavior_dialog.behavior_component
        if behavior!='':
            self.update_behavior_dict(behavior,behavior_component,add_to_db)
        
        
    def update_behavior_dict(self,behavior,component,add_to_db):
        all_behaviors = [self.response_behavior_combobox.itemText(i) for i in range(self.response_behavior_combobox.count())]
        

        if behavior in all_behaviors: 
            behavior_components = self.data['behaviors_dict'][behavior]
            if component not in behavior_components:
                self.data['behaviors_dict'][behavior].append(component)
        else:
            self.data['behaviors_dict'][behavior] = []
            self.data['behaviors_dict'][behavior].append(component)
            self.response_behavior_combobox.addItem(behavior)
        
        if add_to_db:
            all_behaviors = self.data['behaviors_dict_db'].keys()
            if behavior in all_behaviors: 
                behavior_components = self.data['behaviors_dict_db'][behavior]
                if component not in behavior_components:
                    self.data['behaviors_dict_db'][behavior].append(component)
            else:
                self.data['behaviors_dict_db'][behavior] = []
                self.data['behaviors_dict_db'][behavior].append(component)
            
            with open('behaviors_dict.pickle','wb') as f:
                pickle.dump(self.data['behaviors_dict_db'],f)
                
        self.populate_behavior_subcategory_slot()
                
            
    def _stim_df_is_available(self):

        # read the existing stim_table from the output directory
        # check output_dir is provided
        if 'output_dir' not in self.data:
            show_warning_dialog('Output Dir has not been selected!')
            return False
        if not os.path.isdir(self.data['output_dir']):
           show_warning_dialog('Output Dir does not exist!')
           return False
           
        #read stim_table from the output_dir
        stim_file_path = os.path.join(self.data['output_dir'],'stim_table.csv')
          
        if 'df' in self.data.keys():
            self.data['df'].to_csv(stim_file_path)
            self.data['df_path'] = stim_file_path
            self._initiate_stim_table()
            return True
        
        #if there is a file in the output dir
        if os.path.isfile(stim_file_path):
            self.data['df'] = pd.read_csv(stim_file_path)
        else:   #if there is no file, create a new dataframe
            self.data['df'] = pd.DataFrame()

        self.data['df_path'] = stim_file_path
        self._initiate_stim_table()
        return True
        
        
    def open_plot_dialog_slot(self):
        dialog = QDialog()
        plottingapp = PlottingApp()
        plottingapp.setupApp(dialog)
        dialog.exec_()
        
    


          
class WarningDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Error!")

        # Set up the layout
        layout = QVBoxLayout()

        # Create a QLabel to display the warning message
        label = QLabel(message)
        layout.addWidget(label)

        # Create a QPushButton to close the dialog
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.setMinimumSize(300, 100)

def show_warning_dialog(message):
    dialog = WarningDialog(message)
    dialog.exec_()
    
    

def is_item_in_list(item_text, list_widget):
        for index in range(list_widget.count()):
            if list_widget.item(index).text() == item_text:
                return True
        return False



def get_all_items_in_list(list_widget):
    all_items = [list_widget.item(index).text() for index in range(list_widget.count())]
    return all_items
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    MainWindow = QtWidgets.QMainWindow()


    ui = App()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #MainWindow.move(50,50)
    sys.exit(app.exec_())
