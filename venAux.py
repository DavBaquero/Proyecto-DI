from datetime import datetime

import dlgGestionprop
from dlgCalendar import *
import var
import eventos
from dlgGestionprop import Ui_dlgTipoProp


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        var.uicalendar.Calendar.setSelectedDate((QtCore.QDate(ano, mes, dia)))
        var.uicalendar.Calendar.clicked.connect(eventos.Eventos.cargarFecha)


class dlg_Tipo_prop(QtWidgets.QDialog):
    def __init__(self):
        super(dlgGestionprop,self).__init__()
        var.dlggestion = Ui_dlgTipoProp()
        var.dlggestion.setupUi(self)


class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir,self).__init__()