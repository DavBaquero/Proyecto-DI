from datetime import datetime
from dlgCalendar import *
import var
import eventos

class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.today().day
        mes = datetime.today().month
        ano = datetime.today().year

        var.uicalendar.Calendar.setSelectedDate((QtCore.QDate(ano, mes, dia)))
        var.uicalendar.Calendar.clicked.connect(eventos.Eventos.cargarFecha)
