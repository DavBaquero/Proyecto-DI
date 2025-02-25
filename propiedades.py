import csv
import json
import shutil
from datetime import datetime

from PyQt6 import QtWidgets,QtCore

import alquileres
import conexion

import eventos
import facturas
import var


class Propiedades():
    def altaTipopropiedad(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para añadir un tipo de propiedad a la base de datos.
        """
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            registro = conexion.Conexion.altaTipoprop(tipo)
            if registro:
                var.ui.cmbTipoprop.clear()
                var.ui.cmbTipoprop.addItems(registro)
                mbox = eventos.Eventos.crearMensajeInfo("Aviso", "Tipo de propiedad añadido.")
                mbox.exec()
                var.dlggestion.ui.txtGestipoprop.setText("")
            else:
                mbox = eventos.Eventos.crearMensajeError("Error", "Error al añadir tipo de propiedad.")
                mbox.exec()
                var.dlggestion.ui.txtGestipoprop.setText("")
        except Exception as e:
            print("Error alta tipo propiedad" + e)


    def bajaTipopropiedad(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para eliminar un tipo de propiedad de la base de datos.

        """
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            if conexion.Conexion.bajaTipoprop(tipo):
                mbox = eventos.Eventos.crearMensajeInfo("Aviso", "Tipo de propiedad eliminado.")
                mbox.exec()
                eventos.Eventos.cargarTipoprop()
                var.dlggestion.ui.txtGestipoprop.setText("")
            else:
                mbox = eventos.Eventos.crearMensajeError("Error", "Error al eliminar tipo de propiedad.")
                mbox.exec()
        except Exception as e:
            print("Error baja tipo propiedad" + e)

    def altaPropiedad(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para añadir una propiedad a la base de datos.

        """
        try:
            propiedad = [var.ui.txtAltaprop.text(),var.ui.txtDirprop.text().title(),var.ui.cmbProvprop.currentText(),
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

                propiedad.append(var.ui.txtNomeprop.text().title())
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
        """
        :param movil: Número de teléfono móvil
        :type movil: String
        :return: None
        :rtype: None

        Metodo para validar el número de teléfono móvil introducido en la ventana de propiedades.

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para cargar la tabla de propiedades en la ventana de propiedades.

        """
        try:
            var.ui.tablaProp.setRowCount(0)
            listado = conexion.Conexion.listadoPropiedades()
            total = len(listado)
            start_index = var.current_page_prop * var.items_per_page_prop
            end_index = start_index + var.items_per_page_prop
            sublistado = listado[start_index:end_index] if listado else []
            var.ui.tablaProp.setRowCount(len(sublistado))
            if not listado:
                var.ui.tablaProp.setRowCount(1)
                var.ui.tablaProp.setItem(0, 2, QtWidgets.QTableWidgetItem("No hay propiedades de ese tipo"))
                var.ui.tablaProp.item(0, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                for index, registro in enumerate(sublistado):
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
                var.ui.btnAntProp.setEnabled(var.current_page_prop > 0)
                var.ui.btnSigProp.setEnabled(end_index < total)
        except Exception as error:
            print('Error cargaTablaPropiedades: %s ' % str(error))

    @staticmethod
    def cargaOnePropiedad():
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para cargar una propiedad en la ventana de propiedades.

        """
        try:
            fila = var.ui.tablaProp.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOnePropiedad(str(datos[0]))
            listado = [var.ui.lblProp, var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop, var.ui.cmbProvprop,
                       var.ui.cmbMuniprop, var.ui.cmbTipoprop,
                       var.ui.spinHabprop, var.ui.spinBanosprop, var.ui.txtSuperprop, var.ui.txtPrecioAlquilerprop,
                       var.ui.txtPrecioVentaprop,
                       var.ui.txtCpprop, var.ui.areatxtDescriprop, var.ui.rbtDisponprop, var.ui.rbtAlquilprop,
                       var.ui.rbtVentaprop, var.ui.chkInterprop,
                       var.ui.chkAlquilprop, var.ui.chkVentaprop, var.ui.txtNomeprop, var.ui.txtMovilprop]
            listadoVentas = []
            listadoAlquier = []
            for i in range(len(listado)):
                if i in (4, 5, 6):
                    listado[i].setCurrentText(registro[i])
                elif i in (7, 8):
                    listado[i].setValue(int(registro[i]))
                elif i == 13:
                    listado[i].setPlainText(registro[i])
                elif i == 14:
                    listado[i].setChecked(registro[14] == "Disponible")
                elif i == 15:
                    listado[i].setChecked(registro[15] == "Alquilado")
                elif i == 16:
                    listado[i].setChecked(registro[15] == "Vendido")
                elif i in (17, 18, 19):
                    listado[17].setChecked("Intercambio" in registro[14])
                    listado[18].setChecked("Alquiler" in registro[14])
                    listado[19].setChecked("Venta" in registro[14])
                    if "Venta" in registro[14] and "Venta" not in listadoVentas:
                        listadoVentas.append("Venta")
                    if "Alquiler" in registro[14] and "Alquiler" not in listadoAlquier:
                        listadoAlquier.append("Alquiler")
                elif i == 20:
                    listado[i].setText(registro[16])
                elif i == 21:
                    listado[i].setText(registro[17])
                else:
                    listado[i].setText(registro[i])

            listadoVentas.append(registro[0])
            listadoVentas.append(registro[6])
            listadoVentas.append(registro[11])
            listadoVentas.append(registro[3])
            listadoVentas.append(registro[5])

            listadoAlquier.append(registro[0])
            listadoAlquier.append(registro[6])
            listadoAlquier.append(registro[10])
            listadoAlquier.append(registro[3])
            listadoAlquier.append(registro[5])

            if "Disponible" in registro and "Disponible" not in listadoVentas:
                listadoVentas.append("Disponible")
            if "Alquilado" in registro and "Alquilado" not in listadoVentas:
                listadoVentas.append("Alquilado")
            if "Vendido" in registro and "Vendido" not in listadoVentas:
                listadoVentas.append("Vendido")

            if "Disponible" in registro and "Disponible" not in listadoAlquier:
                listadoAlquier.append("Disponible")
            if "Alquilado" in registro and "Alquilado" not in listadoAlquier:
                listadoAlquier.append("Alquilado")
            if "Vendido" in registro and "Vendido" not in listadoAlquier:
                listadoAlquier.append("Vendido")

            if listadoVentas[0] == "Venta" and listadoVentas[6] == "Disponible":
                facturas.Facturas.cargarPropiedadVenta(listadoVentas)

            if listadoAlquier[0] == "Alquiler" and listadoAlquier[6] == "Disponible":
                alquileres.Alquileres.cargarPropiedadAlquiler(listadoAlquier)


            Propiedades.manageRadioButtons()
        except Exception as e:
            print("Error cargando UNA propiedad en propiedades.", e)


    @staticmethod
    def cargaOnePropiedadBusq():
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para cargar una propiedad en la ventana de propiedades cuando se realiza una busqueda.

        """
        try:
            municipio = var.ui.cmbMuniprop.currentText()
            provincia = var.ui.cmbProvprop.currentText()
            registro = conexion.Conexion.datosOnePropiedadBusq(str(municipio),str(provincia))
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
        """
        :param datosPropiedades: Lista con los datos de la propiedad
        :type datosPropiedades: List
        :return: True si no hay campos vacíos, False si hay campos vacíos
        :rtype: Boolean

        Metodo para comprobar si hay campos vacíos en la ventana de propiedades.

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para modificar una propiedad en la base de datos.

        """
        try:
            propiedad = [var.ui.lblProp.text(),var.ui.txtAltaprop.text(),var.ui.txtBajaprop.text(),var.ui.txtDirprop.text().title(),var.ui.cmbProvprop.currentText(),
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

                propiedad.append(var.ui.txtNomeprop.text().title())
                propiedad.append(var.ui.txtMovilprop.text().title())

                if propiedad[2] != "" and propiedad[1] > propiedad[2]:
                    mbox = eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser posterior a la fecha de alta.")
                    mbox.exec()
                elif Propiedades.checkDatosVaciosModifProp(propiedad) and conexion.Conexion.modifProp(propiedad):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso","Se ha modificado la propiedad correctamente.")
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades()
                elif not Propiedades.checkDatosVaciosModifProp(propiedad):
                    mbox = eventos.Eventos.crearMensajeError("Error","Hay algunos campos obligatorios que están vacíos.")
                    mbox.exec()
                else:
                    mbox = eventos.Eventos.crearMensajeError("Error","Se ha producido un error al modificar la propiedad")
                    mbox.exec()

        except Exception as e:
            print("Error modificando cliente en propiedades.", e)

    @staticmethod
    def checkDatosVaciosModifProp(datosPropiedades):
        """

        :param datosPropiedades: Lista con los datos de la propiedad
        :type datosPropiedades: List
        :return: True si no hay campos vacíos, False si hay campos vacíos
        :rtype: Boolean

        Metodo para comprobar si hay campos vacíos en la ventana de propiedades.

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para dar de baja una propiedad en la base de datos.

        """
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
                    mbox = eventos.Eventos.crearMensajeError("Error","No has introducido fecha de baja.")
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades()
                elif conexion.Conexion.bajaPropiedad(datos):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso","Propiedad dada de baja correctamente.")
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades()
                else:
                    mbox = eventos.Eventos.crearMensajeError("Error","La propiedad no está en la base de datos.")
                    mbox.exec()
                    Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("error bajaCliente", e)

    def historicoProp(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para mostrar el historico de una propiedad en la ventana de propiedades.

        """
        try:
            Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("checkbox historico no funciona correcatamente", e)



    @staticmethod
    def validarFechaBaja():
        """
        :param self: None
        :type self: None
        :return: True or False
        :rtype: Boolean

        Metodo para validar la fecha de baja de una propiedad.

        """
        try:
            if var.ui.txtBajaprop.text() == "" or var.ui.txtBajaprop.text() is None:
                return True
            else:
                fecha_baja = datetime.strptime(var.ui.txtBajaprop.text(), "%d/%m/%Y")
                fecha_alta = datetime.strptime(var.ui.txtAltaprop.text(), "%d/%m/%Y")
                if fecha_baja < fecha_alta:
                    return False
                else:
                    return True
        except Exception as e:
            print("Error en validarFechaBaja: ", e)
            return False

    @staticmethod
    def manageChkBox():
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para gestionar los checkbox de la ventana de propiedades.

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para gestionar los radio buttons de la ventana de propiedades.

        """
        if var.ui.txtBajaprop.text() == "":
            var.ui.rbtDisponprop.setEnabled(True)
            var.ui.rbtDisponprop.setChecked(True)
            var.ui.rbtAlquilprop.setChecked(False)
            var.ui.rbtAlquilprop.setEnabled(False)
            var.ui.rbtVentaprop.setChecked(False)
            var.ui.rbtVentaprop.setEnabled(False)
        elif conexion.Conexion.checkPropiedadAlq(var.ui.lblProp.text()):
            var.ui.rbtDisponprop.setChecked(False)
            var.ui.rbtDisponprop.setEnabled(False)
            var.ui.rbtAlquilprop.setEnabled(True)
            var.ui.rbtAlquilprop.setChecked(True)
            var.ui.rbtVentaprop.setChecked(False)
            var.ui.rbtVentaprop.setEnabled(False)
        elif conexion.Conexion.checkPorpiedadVen(var.ui.lblProp.text()):
            var.ui.rbtDisponprop.setChecked(False)
            var.ui.rbtDisponprop.setEnabled(False)
            var.ui.rbtAlquilprop.setChecked(False)
            var.ui.rbtAlquilprop.setEnabled(False)
            var.ui.rbtVentaprop.setEnabled(True)
            var.ui.rbtVentaprop.setChecked(True)

    def exportarCSVProp(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para exportar los datos de las propiedades en un archivo CSV.

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para exportar los datos de las propiedades en un archivo JSON.

        """
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


    def anteriorPropiedad(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para mostrar la página de propiedades anterior en la ventana de propiedades.

        """
        try:
            if var.current_page_prop > 0:
                var.current_page_prop -= 1
            Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("Error anterior propiedad", e)

    def siguientePropiedad(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para mostrar la página de propiedades siguiente en la ventana de propiedades.

        """
        try:
            var.current_page_prop += 1
            Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("Error siguiente propiedad", e)

    def filtrarPropiedades(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para filtrar las propiedades en la ventana de propiedades.

        """
        try:
            Propiedades.cargarTablaPropiedades()
            Propiedades.cargaOnePropiedadBusq()
        except Exception as e:
            print("Error filtrar propiedades", e)

    def cargaMuniInformeProp(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para cargar los municipios en el informe de propiedades.

        """
        registro = conexion.Conexion.cargarMunicipios()
        if registro is None:
            registro = []
        registro.insert(0, "")
        self.ui.cmbInformeMuniProp.setEditable(True)
        self.ui.cmbInformeMuniProp.clear()
        self.ui.cmbInformeMuniProp.addItems(registro)
        completer = QtWidgets.QCompleter(registro, self.ui.cmbInformeMuniProp)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.ui.cmbInformeMuniProp.setCompleter(completer)