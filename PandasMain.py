from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTableView, QMessageBox
import pandas as pd





class PandasModel(QtCore.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
        
    def updateDataFrame(self, df):
        self.beginResetModel()
        self._df = df
        self.endResetModel()
        
    def get_dataframe(self):
        return self._df


class PandasMain(object):
    def __init__(self,dialog):
            super().__init__()
            self.dialog = dialog
            
            self.model = PandasModel()
            self.table = QTableView()
            self.table.setModel(self.model)
        
            self.vLayout = QVBoxLayout(self.dialog)
            self.vLayout.addWidget(self.table)
            
    
    def setup_ui(self, df):
        self.model.updateDataFrame(df)
        self.table.setModel(self.model)
        
    def update_table(self, new_df):
        self.model.updateDataFrame(new_df)
        
        
    def remove_rows(self):
        selected_indexes = self.table.selectionModel().selectedRows()
        if selected_indexes:
            row_index = [selected_indexes[i].row() for i in range(len(selected_indexes))]
            self.model._df = self.model._df.drop(self.model._df.index[row_index]).reset_index(drop=True)
            self.model.updateDataFrame(self.model._df)
        else:
            QMessageBox.warning(self.dialog, "Error", "Please select a row to remove")
            
    def get_dataframe(self):
        return self.model.get_dataframe()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    df_dialog = QtWidgets.QDialog()
    w = Pandas_Main(df_dialog)
    df = pd.read_csv('test.csv')
    w.setup_ui(df)
    sys.exit(app.exec_())