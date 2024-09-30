import sys

from PyQt6 import QtWidgets, QtGui
import conexion
import var


class Eventos():
    def mensajeSalir(self=None):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('img/logo.svg'))
        mbox.setWindowTitle('Salir')
        mbox.setText('¿Desea usted salir?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    def cargarProvincias(self):
        var.ui.cmbProvcli.clear()
        listado = conexion.Conexion().listaProv(self)
        var.ui.cmbProvcli.addItems(listado)

    def cargarMunicipio(self):
        var.ui.cmbMunicli.clear()
        listado = conexion.Conexion().listaMuni(self)
        var.ui.cmbMunicli.addItems(listado)