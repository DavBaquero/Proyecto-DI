import csv
import json
import shutil
from datetime import datetime

from PyQt6 import QtWidgets,QtGui,QtCore

import conexion
from eventos import Eventos
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
                         var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),var.ui.txtPrecioAlquilerprop.text(),
                         var.ui.txtPrecioVentaprop.text(),
                         var.ui.txtCpprop.text(),var.ui.areatxtDescriprop.toPlainText()]

            validarFechaBaja = Propiedades.validarFechaBaja()
            if (validarFechaBaja == False):
                mbox = eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser anterior a la fecha de alta.")
                mbox.exec()
            elif var.ui.txtBajaprop.text().isalpha() or var.ui.txtAltaprop.text().isalpha():
                mbox = eventos.Eventos.crearMensajeError("Error","Las fechas no pueden contener letras.")
                mbox.exec()
            else:
                tipoper = []

                if var.ui.txtBajaprop.text() ==  None:
                    var.ui.txtBajaprop.text.setText("")
                if var.ui.chkAlquilprop.isChecked():
                    tipoper.append(var.ui.chkAlquilprop.text())
                if var.ui.chkVentaprop.isChecked():
                    tipoper.append(var.ui.chkVentaprop.text())
                if var.ui.chkInterprop.isChecked():
                    tipoper.append(var.ui.chkInterprop.text())
                propiedad.append(tipoper)

                if var.ui.rbtDisponprop.isChecked():
                    propiedad.append(var.ui.rbtDisponprop.text())
                elif var.ui.rbtAlquilprop.isChecked():
                    propiedad.append(var.ui.rbtAlquilprop.text())
                elif var.ui.rbtVentaprop.isChecked():
                    propiedad.append(var.ui.rbtVentaprop.text())

                propiedad.append(var.ui.txtNomeprop.text())
                propiedad.append(var.ui.txtMovilprop.text())
                if Propiedades.checkDatosVaciosAltaProp(propiedad) and conexion.Conexion.altaPropiedad(propiedad):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso", "Se ha grabado la propiedad en la base de datos.")
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades()
                elif not Propiedades.checkDatosVaciosAltaProp(propiedad):
                    mbox = eventos.Eventos.crearMensajeError("Aviso", "Hay campos vacíos que deben ser cubiertos.")
                    mbox.exec()
                else:
                    mbox = eventos.Eventos.crearMensajeError("Aviso","Se ha producido un error al grabar la propiedad.")
                    mbox.exec()
        except Exception as e:
            print(str(e))

    @staticmethod
    def checkMovilProp(movil):
        try:
            if eventos.Eventos.validarMovil(movil):
                var.ui.txtMovilprop.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtMovilprop.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtMovilprop.setText(None)
                var.ui.txtMovilprop.setPlaceholderText("móvil no válido")
                var.ui.txtMovilprop.setFocus()
        except Exception as e:
            print("error check movil", e)

    @staticmethod
    def cargarTablaPropiedades():
        try:
            listado = conexion.Conexion.listadoPropiedades()
            index = 0
            var.ui.tablaProp.setRowCount(len(listado))

            for registro in listado:
                var.ui.tablaProp.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaProp.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[5])))
                var.ui.tablaProp.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[6])))
                var.ui.tablaProp.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaProp.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                if registro[10] == "":
                    registro[10] = "-"
                elif registro[11] == "":
                    registro[11] = "-"
                var.ui.tablaProp.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[10]) + "€"))
                var.ui.tablaProp.setItem(index, 6, QtWidgets.QTableWidgetItem(str(registro[11]) + "€"))
                var.ui.tablaProp.setItem(index, 7, QtWidgets.QTableWidgetItem(str(registro[14])))
                var.ui.tablaProp.setItem(index, 8, QtWidgets.QTableWidgetItem(str(registro[2])))


                var.ui.tablaProp.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaProp.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaProp.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaProp.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaProp.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaProp.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaProp.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaProp.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaProp.item(index, 8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                index += 1
        except Exception as error:
            print('Error cargaTablaPropiedades: %s ' % str(error))

    @staticmethod
    def cargaOnePropiedad():
        try:
            fila = var.ui.tablaProp.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOnePropiedad(str(datos[0]))
            listado = [var.ui.lblProp,var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop,var.ui.cmbProvprop,
                       var.ui.cmbMuniprop,var.ui.cmbTipoprop,
                       var.ui.spinHabprop, var.ui.spinBanosprop, var.ui.txtSuperprop,var.ui.txtPrecioAlquilerprop,
                       var.ui.txtPrecioVentaprop,
                       var.ui.txtCpprop,var.ui.areatxtDescriprop, var.ui.rbtDisponprop, var.ui.rbtAlquilprop,var.ui.rbtVentaprop,var.ui.chkInterprop,
                       var.ui.chkAlquilprop,var.ui.chkVentaprop,var.ui.txtNomeprop,var.ui.txtMovilprop]

            for i in range(len(listado)):
                if i in (4,5,6):
                    listado[i].setCurrentText(registro[i])
                elif i in (7,8):
                    listado[i].setValue(int(registro[i]))
                elif i == 13:
                    listado[i].setPlainText(registro[i])
                elif i == 14:
                    listado[i].setChecked(registro[15] == "Disponible")
                elif i == 15:
                    listado[i].setChecked(registro[15] == "Alquilado")
                elif i == 16:
                    listado[i].setChecked(registro[15] == "Vendido")
                elif i in (17,18,19):
                    listado[17].setChecked("Intercambio" in registro[14])
                    listado[18].setChecked("Alquiler" in registro[14])
                    listado[19].setChecked("Venta" in registro[14])
                elif i == 20:
                    listado[i].setText(registro[16])
                elif i == 21:
                    listado[i].setText(registro[17])
                else:
                    listado[i].setText(registro[i])
        except Exception as e:
            print("Error cargando UNA propiedad en propiedades.", e)

    @staticmethod
    def checkDatosVaciosAltaProp(datosPropiedades):
        datos = datosPropiedades[:]
        oberprop= datos.pop(11)
        prealquilerprop = datos.pop(9)
        prevenprop = datos.pop(8)
        banprop = datos.pop(6)
        habprop = datos.pop(5)

        for dato in datos:
            if dato == "" or dato is None:
                return False
        return True

    @staticmethod
    def modifProp():
        try:
            propiedad = [var.ui.lblProp.text(),var.ui.txtAltaprop.text(),var.ui.txtBajaprop.text(),var.ui.txtDirprop.text(),var.ui.cmbProvprop.currentText(),
                         var.ui.cmbMuniprop.currentText(),var.ui.cmbTipoprop.currentText(),
                         var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),var.ui.txtPrecioAlquilerprop.text(),
                         var.ui.txtPrecioVentaprop.text(),
                         var.ui.txtCpprop.text(),var.ui.areatxtDescriprop.toPlainText()]
            validarFechaBaja = Propiedades.validarFechaBaja()
            if (validarFechaBaja == False):
                mbox = eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser anterior a la fecha de alta.")
                mbox.exec()
            elif var.ui.txtBajaprop.text().isalpha() or var.ui.txtAltaprop.text().isalpha():
                mbox = eventos.Eventos.crearMensajeError("Error","Las fechas no pueden contener letras.")
                mbox.exec()
            else:
                tipoOper = []
                if var.ui.chkAlquilprop.isChecked():
                    tipoOper.append(var.ui.chkAlquilprop.text())
                if var.ui.chkVentaprop.isChecked():
                    tipoOper.append(var.ui.chkVentaprop.text())
                if var.ui.chkInterprop.isChecked():
                    tipoOper.append(var.ui.chkInterprop.text())
                propiedad.append(tipoOper)
                if var.ui.rbtDisponprop.isChecked():
                    propiedad.append(var.ui.rbtDisponprop.text())
                elif var.ui.rbtAlquilprop.isChecked():
                    propiedad.append(var.ui.rbtAlquilprop.text())
                elif var.ui.rbtVentaprop.isChecked():
                    propiedad.append(var.ui.rbtVentaprop.text())

                propiedad.append(var.ui.txtNomeprop.text())
                propiedad.append(var.ui.txtMovilprop.text())

                if propiedad[2] != "" and propiedad[1] > propiedad[2]:
                    mbox = eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser posterior a la fecha de alta.")
                    mbox.exec()
                elif Propiedades.checkDatosVaciosModifProp(propiedad) and conexion.Conexion.modifProp(propiedad):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso","Se ha modificado la propiedad correctamente.")
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades()
                elif not Propiedades.checkDatosVaciosModifProp(propiedad):
                    mbox = Eventos.crearMensajeError("Error","Hay algunos campos obligatorios que están vacíos.")
                    mbox.exec()
                else:
                    mbox = Eventos.crearMensajeError("Error","Se ha producido un error al modificar la propiedad")
                    mbox.exec()

        except Exception as e:
            print("Error modificando cliente en propiedades.", e)

    @staticmethod
    def checkDatosVaciosModifProp(datosPropiedades):
        datos = datosPropiedades[:]
        descripcion = datos.pop(13)
        precio_venta = datos.pop(11)
        precio_alquiler = datos.pop(10)
        num_banos = datos.pop(8)
        num_habitaciones = datos.pop(7)
        fecha_baja = datos.pop(2)

        for dato in datos:
            if dato == "" or dato is None:
                return False
        return True

    def bajaProp(self):
        try:
            datos = [var.ui.txtBajaprop.text(), var.ui.lblProp.text()]
            validarFechaBaja = Propiedades.validarFechaBaja()
            if (validarFechaBaja == False):
                mbox = eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser anterior a la fecha de alta.")
                mbox.exec()
            elif var.ui.txtBajaprop.text().isalpha() or var.ui.txtAltaprop.text().isalpha():
                mbox = eventos.Eventos.crearMensajeError("Error","Las fechas no pueden contener letras.")
                mbox.exec()
            else:
                if datos[0] == "":
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowIcon(QtGui.QIcon('img/logo.svg'))
                    mbox.setWindowTitle('Aviso')
                    mbox.setText('No has introducido fecha')
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades()
                elif conexion.Conexion.bajaPropiedad(datos):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowIcon(QtGui.QIcon('img/logo.svg'))
                    mbox.setWindowTitle('Aviso')
                    mbox.setText('Propiedad borrada')
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowIcon(QtGui.QIcon('img/logo.svg'))
                    mbox.setWindowTitle('Aviso')
                    mbox.setText('La propiedad no está en la base de datos')
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("error bajaCliente", e)

    def historicoProp(self):
        try:
            Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("checkbox historico no funciona correcatamente", e)

    @staticmethod
    def filtrar():
        checkeado = var.ui.btnBuscProp.isChecked()
        var.ui.btnBuscProp.setChecked(not checkeado)
        Propiedades.cargarTablaPropiedades()

    @staticmethod
    def validarFechaBaja():
        if var.ui.txtBajaprop.text() == "":
            return True
        elif var.ui.txtBajaprop.text() < var.ui.txtAltaprop.text():
            return False
        else:
            return True

    @staticmethod
    def manageChkBox():
        if var.ui.txtPrecioAlquilerprop.text() == "":
            var.ui.chkAlquilprop.setChecked(False)
            var.ui.chkAlquilprop.setEnabled(False)
        else:
            var.ui.chkAlquilprop.setChecked(True)
            var.ui.chkAlquilprop.setEnabled(True)

        if var.ui.txtPrecioVentaprop.text() == "":
            var.ui.chkVentaprop.setChecked(False)
            var.ui.chkVentaprop.setEnabled(False)
        else:
            var.ui.chkVentaprop.setChecked(True)
            var.ui.chkVentaprop.setEnabled(True)

        if var.ui.txtPrecioVentaprop.text() == "" and var.ui.txtPrecioAlquilerprop.text() == "":
            var.ui.chkInterprop.setChecked(True)
            var.ui.chkInterprop.setEnabled(True)

    @staticmethod
    def manageRadioButtons():
        if var.ui.txtBajaprop.text() == "":
            var.ui.rbtDisponprop.setEnabled(True)
            var.ui.rbtDisponprop.setChecked(True)
            var.ui.rbtAlquilprop.setChecked(False)
            var.ui.rbtVentaprop.setChecked(False)
            var.ui.rbtAlquilprop.setEnabled(False)
            var.ui.rbtVentaprop.setEnabled(False)
        else:
            var.ui.rbtDisponprop.setChecked(False)
            var.ui.rbtDisponprop.setEnabled(False)
            var.ui.rbtAlquilprop.setChecked(True)
            var.ui.rbtAlquilprop.setEnabled(True)
            var.ui.rbtVentaprop.setEnabled(True)

    def exportarCSVProp(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha + "_DatosPropiedades.csv")
            directorio,fichero = var.dlgAbrir.getSaveFileName(None,"Exporta Datos en CSV", file,'.csv')
            if fichero:
                registros = conexion.Conexion.listadoPropiedadesExportar()
                with open(fichero,"w",newline="",encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Codigo","Alta","Baja","Direccion","Provincia","Municipio","Tipo"
                                        ,"Nº Habitaciones", "Nº Baños", "Superficie", "Precio Alquiler", "Precio Compra",
                                     "Codigo Postal", "Observaciones", "Operacion", "Estado", "Propietario", "Movil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero,directorio)
            else:
                mbox = eventos.Eventos.crearMensajeError("Error","No se ha seleccionado ningún archivo.")
                mbox.exec()
        except Exception as e:
            print("Error exportar CSV", e)

    def exportarJSONProp(self):
        fecha = datetime.today()
        fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
        file = str(fecha + "_DatosPropiedades.json")
        directorio,fichero = var.dlgAbrir.getSaveFileName(None,"Exporta Datos en JSON", file,'.json')
        if fichero:
            keys =["Codigo","Alta","Baja","Direccion","Provincia","Municipio","Tipo"
                ,"Nº Habitaciones", "Nº Baños", "Superficie", "Precio Alquiler", "Precio Compra",
                  "Codigo Postal", "Observaciones", "Operacion", "Estado", "Propietario", "Movil"]
            registros = conexion.Conexion.listadoPropiedadesExportar()
            lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
            with open(fichero,"w",newline="",encoding="utf-8") as jsonfile:
                json.dump(lista_propiedades,jsonfile,ensure_ascii=False,indent=4)
            shutil.move(fichero,directorio)

        else:
            mbox = eventos.Eventos.crearMensajeError("Error","No se ha seleccionado ningún archivo.")
            mbox.exec()