from PyQt6 import QtWidgets,QtGui

import conexion
import eventos
import var


class Propiedades():
    def altaTipopropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            registro = conexion.Conexion.altaTipoprop(tipo)
            if registro:
                var.ui.cmbTipoprop.clear()
                var.ui.cmbTipoprop.addItems(registro)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/icono.svg'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Tipo de propiedad añadida.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                var.dlggestion.ui.txtGestipoprop.setText("")
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/icono.svg'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Error al añadir tipo de propiedad añadida.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                var.dlggestion.ui.txtGestipoprop.setText("")
        except Exception as e:
            print("Error alta tipo propiedad" + e)


    def bajaTipopropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            if conexion.Conexion.bajaTipoprop(tipo):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/icono.svg'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Tipo de propiedad eliminada.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                eventos.Eventos.cargarTipoprop()
                var.dlggestion.ui.txtGestipoprop.setText("")
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/icono.svg'))
                mbox.setWindowTitle('Aviso')
                mbox.setText("Error al eliminar tipo de propiedad.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as e:
            print("Error baja tipo propiedad" + e)

    def altaPropiedad(self):
        try:
            propiedad = [var.ui.txtAltaprop.text(),var.ui.txtDirprop.text(),var.ui.cmbProvprop.currentText(),
                         var.ui.cmbMuniprop.currentText(),var.ui.cmbTipoprop.currentText(),
                         var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),
                         var.ui.txtPrecioAlquilerprop.text(), var.ui.txtPrecioVentaprop.text(),
                         var.ui.txtCpprop.text(),var.ui.areatxtDescriprop.toPlainText()]
            tipoper = []

            if var.ui.chkAlquilprop.isChecked():
                tipoper.append(var.ui.chkAlquilprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipoper.append(var.ui.chkVentaprop.text())
            if var.ui.chkInterprop.isChecked():
                tipoper.append(var.ui.chkInterprop.text())
            propiedad.append(tipoper)

            if var.ui.chkInterprop.isChecked():
                propiedad.append(var.ui.chkInterprop.text())
            elif var.ui.rbtAlquilprop.isChecked():
                propiedad.append(var.ui.rbtAlquilprop.text())
            elif var.ui.rbtVentaprop.isChecked():
                propiedad.append(var.ui.rbtVentaprop.text())

            propiedad.append(var.ui.txtNomeprop.text())
            propiedad.append(var.ui.txtMovilprop.text())
            conexion.Conexion.altaPropiedad()
        except Exception as e:
            print(str(e))