from datetime import datetime

import dlgGestipoprop
from dlgAbout import Ui_venAcercaDe
from dlgGestipoprop import Ui_dlgGestipoprop
import propiedades
from dlgCalendar import *
import var
import eventos


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
        super(dlg_Tipo_prop,self).__init__()
        self.ui = Ui_dlgGestipoprop()
        self.ui.setupUi(self)
        self.ui.btnAltatipoprop.clicked.connect(propiedades.Propiedades.altaTipopropiedad)
        self.ui.btnDeltipoprop.clicked.connect(propiedades.Propiedades.bajaTipopropiedad)


class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir,self).__init__()

class dlg_About(QtWidgets.QDialog):
    def __init__(self):
        super(dlg_About,self).__init__()
        self.ui = Ui_venAcercaDe()
        self.ui.setupUi(self)
        self.ui.btnCerrarAbout.clicked.connect(eventos.Eventos.cerrarAcercaDe)