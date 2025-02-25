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
class Clientes:

    def checkDNI(dni):
        """
        :param dni: Es el dni del cliente
        :type dni: String
        :return: None
        :rtype: None

        Metodo encargado de comprobar si el DNI introducido es válido

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de dar de alta un cliente en la base de datos

        """
        try:
            nuevocli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text().title(), var.ui.txtNomcli.text().title(),
                     var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text().title(), var.ui.cmbProvcli.currentText(),
                     var.ui.cmbMunicli.currentText(), var.ui.txtBajacli.text()]

            posicionObl = [0,1,2,3,5,7,8]
            obligatorios = [nuevocli[i] for i in posicionObl]

            for i in obligatorios:
                if i == '':
                    QtWidgets.QMessageBox.critical(None, "Error", "Falta un dato obligatorio")
                    return

            if conexion.Conexion.altaCliente(nuevocli):
                mbox = eventos.Eventos.crearMensajeInfo("Aviso","Cliente dado de alta")
                mbox.exec()
                Clientes.cargaTablaClientes(self)
            else:
                QtWidgets.QMessageBox.critical(None, "Error","Error al dar alta")

        except Exception as e:
            print("Error alta cliente ", e)

    def checkEmail(mail):
        """
        :param mail: Es el email del cliente
        :type mail: String
        :return: None
        :rtype: None

        Metodo encargado de comprobar si el email introducido es válido

        """
        try:
            mail = str(var.ui.txtEmailcli.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailcli.setStyleSheet('background-color: whitesmoke;')
                var.ui.txtEmailcli.setText(mail.lower())

            else:
                var.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setText("correo no válido")
                var.ui.txtEmailcli.setFocus()

        except Exception as error:
            print("error check cliente", error)

    def checkMovil(movil):
        """
        :param movil: Es el movil del cliente
        :type movil: String
        :return: None
        :rtype: None

        Metodo encargado de comprobar si el movil introducido es válido

        """
        try:
            tlf = str(var.ui.txtMovilcli.text())
            if eventos.Eventos.validarMovil(tlf):
                var.ui.txtMovilcli.setStyleSheet('background-color: whitesmoke;')

            else:
                var.ui.txtMovilcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilcli.setText(None)
                var.ui.txtMovilcli.setText("Movil no valido")
                var.ui.txtMovilcli.setFocus()

        except Exception as error:
            print("error check cliente", error)

    def cargaTablaClientes(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de cargar la tabla de clientes con los datos de la base de datos

        """
        try:
            var.ui.tablaClientes.setRowCount(0)
            listado = conexion.Conexion.listadoClientes()
            total = len(listado)
            # listado = conexionserver.ConexionServer.listadoClientes()
            start_index = var.current_page_cli * var.items_per_page_cli
            end_index = start_index + var.items_per_page_cli
            sublista = listado[start_index:end_index] if listado else []
            var.ui.tablaClientes.setRowCount(len(sublista))
            if not listado:
                var.ui.tablaClientes.setRowCount(1)
                var.ui.tablaClientes.setItem(0, 3, QtWidgets.QTableWidgetItem("No se encuentra el cliente"))
                var.ui.tablaClientes.item(0, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                for index, registro in enumerate (sublista):
                    var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(registro[0]))
                    var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[2]))
                    var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[3]))
                    var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(" " +" " +registro[5]+" " + " "))
                    var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(registro[7]))
                    var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(registro[8]))
                    var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem(registro[9]))

                    if var.ui.tablaClientes.item(index, 0):
                        var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    if var.ui.tablaClientes.item(index, 1):
                        var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    if var.ui.tablaClientes.item(index, 2):
                        var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                    if var.ui.tablaClientes.item(index, 3):
                        var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    if var.ui.tablaClientes.item(index, 4):
                        var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    if var.ui.tablaClientes.item(index, 5):
                        var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                    if var.ui.tablaClientes.item(index, 6):
                        var.ui.tablaClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                var.ui.btnSigCli.setEnabled(end_index < total)
                var.ui.btnAntCli.setEnabled(var.current_page_cli > 0)
        except Exception as e:
            print("Error carga tabla clientes ",e)

    def cargaOneCliente(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de cargar los datos de un cliente en los campos de texto

        """
        try:
            fila = var.ui.tablaClientes.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOneCliente(datos[0])
            listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli,
                        var.ui.txtNomcli,
                        var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli,
                        var.ui.cmbProvcli,
                        var.ui.cmbMunicli, var.ui.txtBajacli]
            for i in range(len(listado)):
                if i == 7 or i == 8:
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
            var.ui.txtdniclifac.setText(registro[0])
            var.ui.txtnomeclifac.setText(registro[3])
            var.ui.txtapelclifac.setText(registro[2])

            var.ui.txtnomeclialq.setText(registro[3])
            var.ui.txtdniclialq.setText(registro[0])
            var.ui.txtapelclialq.setText(registro[2])

            #Clientes.cargaCliente(registro)

        except Exception as error:
            print("Error carga cliente ", error)

    def cargaOneClienteBusq(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de cargar los datos de un cliente en los campos de texto cuando se filtra

        """
        try:
            dni = var.ui.txtDnicli.text().upper()
            registro = conexion.Conexion.datosOneCliente(str(dni))
            listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli,
                       var.ui.txtNomcli,
                       var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli,
                       var.ui.cmbProvcli,
                       var.ui.cmbMunicli, var.ui.txtBajacli]
            for i in range(len(listado)):
                if i == 7 or i == 8:
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
            #Clientes.cargaCliente(registro)

        except Exception as error:
            print("Error carga cliente ", error)

    def modifCliente(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de modificar los datos de un cliente en la base de datos

        """
        try:
            modifcli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text().title(),
                        var.ui.txtNomcli.text().title(),
                        var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text().title(),
                        var.ui.cmbProvcli.currentText(),
                        var.ui.cmbMunicli.currentText(), var.ui.txtBajacli.text()]
            validarFechaBaja = Clientes.validarFechaBaja()
            if (validarFechaBaja == False):
                mbox = eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser anterior a la fecha de alta.")
                mbox.exec()
            elif var.ui.txtBajaprop.text().isalpha() or var.ui.txtAltaprop.text().isalpha():
                mbox = eventos.Eventos.crearMensajeError("Error","Las fechas no pueden contener letras.")
                mbox.exec()
            else:
                if conexion.Conexion.modifiCliente(modifcli):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso","Cliente modificado")
                    mbox.exec()
                    Clientes.cargaTablaClientes(self)
                else:
                    mbox = eventos.Eventos.crearMensajeError("Error","Error al modificar cliente")
                    mbox.exec()
                    Clientes.cargaTablaClientes(self)

                clientes.Clientes.cargaTablaClientes(self)
        except Exception as e:
            print("Error al modificar cliente ", e)

    def bajaCliente(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de dar de baja un cliente en la base de datos

        """
        try:
            datos = [var.ui.txtBajacli.text(), var.ui.txtDnicli.text()]
            validarFechaBaja = Clientes.validarFechaBaja()
            if (validarFechaBaja == False):
                mbox = eventos.Eventos.crearMensajeError("Error","La fecha de baja no puede ser anterior a la fecha de alta.")
                mbox.exec()
            elif var.ui.txtBajaprop.text().isalpha() or var.ui.txtAltaprop.text().isalpha():
                mbox = eventos.Eventos.crearMensajeError("Error","Las fechas no pueden contener letras.")
                mbox.exec()
            else:
                if conexion.Conexion.bajaCliente(datos):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso","Cliente dado de baja")
                    mbox.exec()
                    Clientes.cargaTablaClientes(self)
                else:
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso","El cliente no está en la base de datos")
                    mbox.exec()
                    Clientes.cargaTablaClientes(self)
        except Exception as e:
            print("error bajaCliente", e)

    def historicoCli(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de asignar si se muestra el historico de clientes en la tabla

        """
        try:
            if var.ui.chkHistoriacli.isChecked():
                var.historicocli = 0
            else:
                var.historicocli = 1
            Clientes.cargaTablaClientes(self)
        except Exception as e:
            print("Error en historicocli", e)


    def exportarCSVCli(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de exportar los datos de los clientes en un archivo CSV

        """
        try:
            fecha = datetime.datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha + "_DatosClientes.csv")
            directorio,fichero = var.dlgAbrir.getSaveFileName(None,"Exporta Datos en CSV", file,'.csv')
            if fichero:
                registros = conexion.Conexion.ListadoClientesExportar()
                with open(fichero,"w",newline="",encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["DNI","Fecha Alta","Apellidos","Nombre","Email","Movil","Direccion","Provincia","Municipio","Fecha Baja"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero,directorio)
            else:
                mbox = eventos.Eventos.crearMensajeError("Error","No se ha seleccionado ningún archivo.")
                mbox.exec()
        except Exception as e:
            print("Error exportar CSV", e)

    def exportarJSONCli(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de exportar los datos de los clientes en un archivo JSON

        """
        fecha = datetime.datetime.today()
        fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
        file = str(fecha + "_DatosClientes.json")
        directorio,fichero = var.dlgAbrir.getSaveFileName(None,"Exporta Datos en JSON", file,'.json')
        if fichero:
            keys =["DNI","Fecha Alta","Apellidos","Nombre","Email","Movil","Direccion","Provincia","Municipio","Fecha Baja"]
            registros = conexion.Conexion.listadoPropiedadesExportar()
            lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
            with open(fichero,"w",newline="",encoding="utf-8") as jsonfile:
                json.dump(lista_propiedades,jsonfile,ensure_ascii=False,indent=4)
            shutil.move(fichero,directorio)

        else:
            mbox = eventos.Eventos.crearMensajeError("Error","No se ha seleccionado ningún archivo.")
            mbox.exec()


    def anteriorCliente(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de mostrar la página de clientes anterior en la tabla

        """
        if var.current_page_cli > 0:
            var.current_page_cli -= 1
        Clientes.cargaTablaClientes(self)


    def siguienteCliente(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de mostrar la página de clientes siguiente en la tabla

        """
        var.current_page_cli += 1
        Clientes.cargaTablaClientes(self)

    @staticmethod
    def validarFechaBaja():
        """
        :param None: None
        :type None: None
        :return: True or False
        :rtype: Boolean

        Metodo encargado de validar si la fecha de baja es válida

        """
        try:
            if var.ui.txtBajacli.text() == "" or var.ui.txtBajacli.text() is None:
                return True
            else:
                fecha_baja = datetime.datetime.strptime(var.ui.txtBajacli.text(), "%d/%m/%Y")
                fecha_alta = datetime.datetime.strptime(var.ui.txtAltacli.text(), "%d/%m/%Y")
                if fecha_baja < fecha_alta:
                    return False
                else:
                    return True
        except Exception as e:
            print("Error en validarFechaBaja: ", e)
            return False


    def filtrar(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo encargado de filtrar los clientes en la tabla
        """
        Clientes.cargaTablaClientes(self)
        Clientes.cargaOneClienteBusq(self)
