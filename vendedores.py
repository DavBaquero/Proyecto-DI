import csv
import datetime
import json
import shutil
import time

from PyQt6 import QtWidgets,QtGui, QtCore

import clientes
import conexion
import conexionserver
import eventos
import var
from eventos import Eventos


class Vendedores:
    def altaVendedores(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para dar de alta un vendedor en la base de datos

        """
        try:
            nuevovendedor = [var.ui.txtDNIVen.text(), var.ui.txtNomVen.text().title(), var.ui.txtAltaVen.text(), var.ui.txtBajaVen.text(),
                        var.ui.txtMovilVen.text(), var.ui.txtMailVen.text(), var.ui.cmbDelegVen.currentText()]

            posicionObl = [0,1,4,6]
            obligatorios = [nuevovendedor[i] for i in posicionObl]

            for i in obligatorios:
                if i == '':
                    QtWidgets.QMessageBox.critical(None, "Error", "Falta un dato obligatorio")
                    return
            if conexion.Conexion.altaVendedor(nuevovendedor):
                mbox = eventos.Eventos.crearMensajeInfo("Aviso","Vendedor dado de alta")
                mbox.exec()
            else:
                QtWidgets.QMessageBox.critical(None, "Error","Error al dar alta, el dni puede ya haber sido introducido")

            Vendedores.cargaTablaVendedores(self)
        except Exception as e:
            print("Error alta cliente ", e)

    def checkDNIven(dni):
        """
        :param dni: DNI del vendedor
        :type dni: String
        :return: None
        :rtype: None

        Metodo para comprobar si el DNI introducido es correcto

        """
        try:
            dni = str(dni).upper()
            var.ui.txtDNIVen.setText(str(dni))
            check = eventos.Eventos.validarDNIven(dni)
            if check:
                var.ui.txtDNIVen.setStyleSheet("background-color: rgb(255, 251, 193);")
            else:
                var.ui.txtDNIVen.setStyleSheet("background-color: #FFC0CB;")
                var.ui.txtDNIVen.setText(None)
                var.ui.txtDNIVen.setFocus()
        except Exception as e:
            print("Error check cliente ", e)


    def checkEmailven(mail):
        """
        :param mail: Email del vendedor
        :type mail: String
        :return: None
        :rtype: None

        Metodo para comprobar si el email introducido es correcto

        """
        try:
            mail = str(var.ui.txtMailVen.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtMailVen.setStyleSheet('background-color: whitesmoke;')
                var.ui.txtMailVen.setText(mail.lower())

            else:
                var.ui.txtMailVen.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMailVen.setText(None)
                var.ui.txtMailVen.setText("correo no válido")
                var.ui.txtMailVen.setFocus()

        except Exception as error:
            print("error check cliente", error)

    def checkMovilven(movil):
        """
        :param movil: Movil del vendedor
        :type movil: String
        :return: None
        :rtype: None

        Metodo para comprobar si el movil introducido es correcto

        """
        try:
            tlf = str(var.ui.txtMovilVen.text())
            if eventos.Eventos.validarMovil(tlf):
                var.ui.txtMovilVen.setStyleSheet('background-color: whitesmoke;')

            else:
                var.ui.txtMovilVen.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilVen.setText(None)
                var.ui.txtMovilVen.setText("Movil no valido")
                var.ui.txtMovilVen.setFocus()

        except Exception as error:
            print("error check cliente", error)


    def cargaTablaVendedores(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para cargar la tabla de vendedores

        """
        try:
            listado = conexion.Conexion.listadoVendedores()
            total = len(listado)
            var.ui.tablaVendedores.setRowCount(total)
            if not listado:
                var.ui.tablaVendedores.setRowCount(1)
                var.ui.tablaVendedores.setItem(0, 3, QtWidgets.QTableWidgetItem("No se encuentra el cliente"))
                var.ui.tablaVendedores.item(0, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                for index, registro in enumerate (listado):
                    var.ui.tablaVendedores.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                    var.ui.tablaVendedores.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[1]))
                    var.ui.tablaVendedores.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[2]))
                    var.ui.tablaVendedores.setItem(index, 3, QtWidgets.QTableWidgetItem(" " +" " +registro[3]+" " + " "))

                    if var.ui.tablaVendedores.item(index, 0):
                        var.ui.tablaVendedores.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                    if var.ui.tablaVendedores.item(index, 1):
                        var.ui.tablaVendedores.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                    if var.ui.tablaVendedores.item(index, 2):
                        var.ui.tablaVendedores.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                    if var.ui.tablaVendedores.item(index, 3):
                        var.ui.tablaVendedores.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
        except Exception as e:
            print("Error carga tabla clientes ",e)


    def modifVen(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para modificar un vendedor

        """
        try:
            nuevovendedor = [var.ui.lblCodVen.text(), var.ui.txtNomVen.text().title() ,var.ui.txtAltaVen.text(), var.ui.txtBajaVen.text(),
                             var.ui.txtMovilVen.text(), var.ui.txtMailVen.text(), var.ui.cmbDelegVen.currentText()]
            validarFechaBaja = Vendedores.validarFechaBaja()
            if (validarFechaBaja == False):
                mbox = eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser anterior a la fecha de alta.")
                mbox.exec()
            elif var.ui.txtBajaVen.text().isalpha() or var.ui.txtAltaVen.text().isalpha():
                mbox = eventos.Eventos.crearMensajeError("Error","Las fechas no pueden contener letras.")
                mbox.exec()
            else:
                if conexion.Conexion.modifiVendedores(nuevovendedor):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso","Vendedor modificado")
                    mbox.exec()
                    Vendedores.cargaTablaVendedores(self)
                else:
                    mbox = eventos.Eventos.crearMensajeError("Error","Error al modificar vendedor")
                    mbox.exec()
                    Vendedores.cargaTablaVendedores(self)

                Vendedores.cargaTablaVendedores(self)
        except Exception as e:
            print("Error al modificar cliente ", e)

    def bajaVendedor(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para dar de baja un vendedor

        """
        try:
            datos = [var.ui.txtBajaVen.text(), var.ui.lblCodVen.text()]
            validarFechaBaja = Vendedores.validarFechaBaja()
            if (validarFechaBaja == False):
                mbox = eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser anterior a la fecha de alta.")
                mbox.exec()
            elif var.ui.txtBajaVen.text().isalpha() or var.ui.txtAltaVen.text().isalpha():
                mbox = eventos.Eventos.crearMensajeError("Error","Las fechas no pueden contener letras.")
                mbox.exec()
            else:
                if conexion.Conexion.bajaVendedor(datos):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso","Vendedor dado de baja")
                    mbox.exec()
                    Vendedores.cargaTablaVendedores(self)
                else:
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso","El vendedor no está en la base de datos")
                    mbox.exec()
                    Vendedores.cargaTablaVendedores(self)
        except Exception as e:
            print("error bajaCliente", e)

    @staticmethod
    def validarFechaBaja():
        """

        :param self: None
        :type self: None
        :return: True or False
        :rtype: Boolean

        Metodo para validar la fecha de baja

        """
        try:
            if var.ui.txtBajaVen.text() == "" or var.ui.txtBajaVen.text() is None:
                return True
            else:
                fecha_baja = datetime.datetime.strptime(var.ui.txtBajaVen.text(), "%d/%m/%Y")
                fecha_alta = datetime.datetime.strptime(var.ui.txtAltaVen.text(), "%d/%m/%Y")
                if fecha_baja < fecha_alta:
                    return False
                else:
                    return True
        except Exception as e:
            print("Error en validarFechaBaja: ", e)
            return False

    def cargaOneVendedor(self):
        """

        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo para cargar un vendedor

        """
        try:
            fila = var.ui.tablaVendedores.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOneVendedor(str(datos[0]))
            listado = [var.ui.lblCodVen, var.ui.txtDNIVen,var.ui.txtNomVen, var.ui.txtAltaVen, var.ui.txtBajaVen,
                             var.ui.txtMovilVen, var.ui.txtMailVen, var.ui.cmbDelegVen]
            for i in range(len(listado)):
                if i == 7:
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
            #Clientes.cargaCliente(registro)
            var.ui.txtidvenfac.setText(str(registro[0]))
            var.ui.txtidvenalq.setText(str(registro[0]))

        except Exception as error:
            print("Error carga un vendedor ", error)