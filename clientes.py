from tabnanny import check

from PyQt6 import QtWidgets

import eventos
import var
class Clientes:

    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            check = eventos.Eventos.validarDNIcli(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet("background-color: rgb(255, 251, 193);")
            else:
                var.ui.txtDnicli.setStyleSheet("background-color: #FFC0CB;")
                var.ui.txtDnicli.setText(None)
                var.ui.txtDnicli.setFocus()
        except Exception as e:
            print("Error check cliente ", e)

    def altaCliente(self):
        dni = var.ui.txtDnicli.text()
        print(dni)