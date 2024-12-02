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
        try:
            nuevocli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(),
                     var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(), var.ui.cmbProvcli.currentText(),
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
        try:
            listado = conexion.Conexion.listadoClientes(self)
            # listado = conexionserver.ConexionServer.listadoClientes()
            index = 0
            var.ui.tablaClientes.setRowCount(len(listado))
            if not listado:
                var.ui.tablaClientes.setRowCount(1)
                var.ui.tablaClientes.setItem(0, 3, QtWidgets.QTableWidgetItem("No se encuentra el cliente"))
                var.ui.tablaClientes.item(0, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                for registro in listado:
                    var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(registro[0]))
                    var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[2]))
                    var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[3]))
                    var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(" " +" " +registro[5]+" " + " "))
                    var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(registro[7]))
                    var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(registro[8]))
                    var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem(registro[9]))

                    var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                    var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                    var.ui.tablaClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                    index += 1

        except Exception as e:
            print("Error carga tabla clientes ")

    def cargaOneCliente(self):
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
            #Clientes.cargaCliente(registro)

        except Exception as error:
            print("Error carga cliente ", error)

    def modifCliente(self):
        try:
            modifcli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(),
                        var.ui.txtNomcli.text(),
                        var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(),
                        var.ui.cmbProvcli.currentText(),
                        var.ui.cmbMunicli.currentText(), var.ui.txtBajacli.text()]
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
        try:
            datos = [var.ui.txtBajacli.text(), var.ui.txtDnicli.text()]
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
        try:
            if var.ui.chkHistoriacli.isChecked():
                var.historicocli = 0
            else:
                var.historicocli = 1
            Clientes.cargaTablaClientes(self)
        except Exception as e:
            print("Error en historicocli", e)


    def exportarCSVCli(self):
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
        try:
            if var.ui.tablaClientes.currentRow() == -1:
                var.ui.tablaClientes.selectRow(0)
            else:
                var.ui.tablaClientes.selectRow(var.ui.tablaClientes.currentRow()-1)
            Clientes.cargaOneCliente(self)
        except Exception as e:
            print("Error anterior cliente ", e)


    def siguienteCliente(self):
        try:
            if var.ui.tablaClientes.currentRow() == -1:
                var.ui.tablaClientes.selectRow(0)
            else:
                var.ui.tablaClientes.selectRow(var.ui.tablaClientes.currentRow()+1)
            Clientes.cargaOneCliente(self)
        except Exception as e:
            print("Error siguiente cliente ", e)
