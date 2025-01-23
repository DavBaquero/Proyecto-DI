import os
import sys
from PyQt6 import QtWidgets, QtGui
import conexion
import propiedades
import var
import time
import re
from datetime import datetime
import locale
import clientes
import conexionserver
import zipfile
import shutil

locale.setlocale(locale.LC_TIME,'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY,'es_ES.UTF-8')

class Eventos():
    def mensajeSalir(self=None):
        mbox = Eventos.crearMensajeSalida('Salir',"¿Desea salir?")
        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    @staticmethod
    def crearMensajeSalida(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('./img/logo.svg'))
        mbox.setText(mensaje)
        mbox.setWindowTitle(titulo_ventana)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
        return mbox

    @staticmethod
    def crearMensajeInfo(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        mbox.setWindowIcon(QtGui.QIcon('img/logo.svg'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        return mbox

    @staticmethod
    def crearMensajeError(titulo_ventana, mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mbox.setWindowIcon(QtGui.QIcon('img/logo.svg'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        return mbox


    '''
        Zona general
    '''

    def abrirCalendar(pan, btn):
        try:
            var.panel = pan
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    def cargarFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.panel == 0 and var.btn == 0:
                var.ui.txtAltacli.setText(str(data))
            elif var.panel == 0 and var.btn == 1:
                var.ui.txtBajacli.setText(str(data))
            elif var.panel == 1 and var.btn == 0:
                var.ui.txtAltaprop.setText(str(data))
            elif var.panel == 1 and var.btn == 1:
                var.ui.txtBajaprop.setText(str(data))
            elif var.panel == 2 and var.btn == 0:
                var.ui.txtAltaVen.setText(str(data))
            elif var.panel == 2 and var.btn == 1:
                var.ui.txtBajaVen.setText(str(data))
            elif var.panel == 3 and var.btn == 0:
                var.ui.txtFechaFactura.setText(str(data))

            time.sleep(0.125)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def crearBackup(self):
        try:
            fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            copia = str(fecha)+'_backup.zip'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Guardar Copia Seguridad", copia, '.zip')
            if var.dlgAbrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero, 'w')
                fichzip.write("bbdd.sqlite",os.path.basename("bbdd.sqlite"),zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero, directorio)
                mbox = Eventos.crearMensajeInfo("Crear Copia de Seguridad", "Copia de seguridad creada.")
                mbox.exec()
        except Exception as error:
            print("error en crear backup: ", error)

    def restaurarBackup(self):
        try:
            filename = var.dlgAbrir.getOpenFileName(None, "Restaurar Copia Seguridad", "", "*.zip;;All Files (*)")
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
                mbox = Eventos.crearMensajeInfo("Restaurar Copia de Seguridad", "Copia de seguridad restaurada.")
                mbox.exec()
                conexion.Conexion.db_conexion()
                Eventos.cargarProvincias(self)
                clientes.Clientes.cargaTablaClientes()
        except Exception as error:
            print("error en restaurar backup: ", error)

    def limpiarPanel(self):
        try:
            current_index = var.ui.panPrincipal.currentIndex()

            if current_index == 0:
                objetospanel = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                                var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli,
                                var.ui.cmbMunicli, var.ui.txtBajacli]

                for i, dato in enumerate(objetospanel):
                    if i not in {7, 8}:
                        dato.setText("")
                Eventos.cargarProvincias(self)

            elif current_index == 1:
                propiedad = [var.ui.lblProp, var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop,
                             var.ui.cmbProvprop, var.ui.cmbMuniprop, var.ui.cmbTipoprop, var.ui.spinHabprop,
                             var.ui.spinBanosprop, var.ui.txtSuperprop, var.ui.txtPrecioAlquilerprop,
                             var.ui.txtPrecioVentaprop, var.ui.txtCpprop, var.ui.areatxtDescriprop,
                             var.ui.rbtDisponprop, var.ui.rbtAlquilprop, var.ui.rbtVentaprop, var.ui.chkInterprop,
                             var.ui.chkAlquilprop, var.ui.chkVentaprop, var.ui.txtNomeprop, var.ui.txtMovilprop]

                for i, dato in enumerate(propiedad):
                    if i not in {4, 5, 6, 7, 8, 14, 15, 16, 17, 18, 19}:
                        dato.setText("")
                    if i in {7,8}:
                        dato.setValue(0)
                    if i in {14}:
                        dato.setChecked(True)
                    if i in {15, 16}:
                        dato.setChecked(False)
                    if i in {17, 18, 19}:
                        dato.setChecked(False)


                Eventos.cargarProvprop(self)
                Eventos.cargarTipoprop()
            elif current_index == 2:
                vendedor = [var.ui.lblCodVen, var.ui.txtDNIVen, var.ui.txtNomVen, var.ui.txtAltaVen,
                            var.ui.txtBajaVen, var.ui.txtMovilVen, var.ui.txtMailVen, var.ui.cmbDelegVen]

                for i, dato in enumerate(vendedor):
                    if i != 7:
                        dato.setText("")
                    else:
                        dato.setCurrentIndex(0)

                Eventos.cargarDelegacion(self)
            elif current_index == 3:
                ventas = [var.ui.lblNumFactura, var.ui.txtdniclifac, var.ui.txtFechaFactura, var.ui.txtnomeclifac, var.ui.txtapelclifac,
                          var.ui.txtidvenfac, var.ui.txtcodpropfac, var.ui.txttipopropfac, var.ui.txtpreciofac, var.ui.txtmunipropfac,
                          var.ui.txtdirpropfac]
                for i, dato in enumerate(ventas):
                    if i != 2:
                        dato.setText("")
                    else:
                        dato.setText(datetime.today().strftime('%d/%m/%Y'))

            else:
                print("panPrincipal es nulo")
        except Exception as e:
            print(f"Se ha producido una excepción: {e}")

    def abrirAbout(self):
        try:
            var.dlgabout.show()
        except Exception as e:
            print("error en abrir about: ", e)

    def cerrarAcercaDe(self):
        try:
            var.dlgabout.close()
        except Exception as e:
            print("error en cerrar acerca de: ", e)

    def filtrar(self):
        if var.ui.panPrincipal.currentIndex() == 0:
            checkeado = var.ui.btnFiltrarCli.isChecked()
            var.ui.btnFiltrarCli.setChecked(not checkeado)
            clientes.Clientes.cargaTablaClientes(self)
            clientes.Clientes.cargaOneClienteBusq(self)
        elif var.ui.panPrincipal.currentIndex() == 1:
            checkeado = var.ui.btnBuscProp.isChecked()
            var.ui.btnBuscProp.setChecked(not checkeado)
            propiedades.Propiedades.cargarTablaPropiedades()



    '''
        Zona clientes
    '''
    def cargarProvincias(self):
        var.ui.cmbProvcli.clear()
        listado = conexion.Conexion().listaProv(self)
        # listado = conexionserver.ConexionServer.listaProv()
        var.ui.cmbProvcli.addItems(listado)

    def cargarMunicipio(self):
        var.ui.cmbMunicli.clear()
        provActual = var.ui.cmbProvcli.currentText()
        listado = conexion.Conexion().listaMuni(provActual)
        # listado = conexionserver.ConexionServer.listaProv()
        var.ui.cmbMunicli.addItems(listado)

    def validarDNIcli(dni):
        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as error:
            print("error en validar dni ", error)

    def validarMail(mail):
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, mail) or mail == '':
            return True
        else:
            return False

    def validarMovil(movil):
        regex = r'^(6\d{8}|7\d{8})$'
        if (re.match(regex, movil) and len(movil) == 9) or (movil == ''):
            return True
        else:
            return False

    def resizeTablaClientes(self):
        try:
            header = var.ui.tablaClientes.horizontalHeader()
            for i in range(header.count()):
                if i not in (0,3,6):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaClientes.horizontalHeaderItem(i)
                if header_items is not None:
                    font = header_items.font()
                    font.setBold(True)
                    header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    '''
        Zona de propiedades
    '''
    @staticmethod
    def abrir_informeProp():
        try:
            var.dlgInformeProp.show()
        except Exception as e:
            print("error en abrir informe propiedades: ", e)

    def cargarProvprop(self):
        var.ui.cmbProvprop.clear()
        listado = conexion.Conexion().listaProv(self)
        var.ui.cmbProvprop.addItems(listado)

    def cargarMuniprop(self):
        var.ui.cmbMuniprop.clear()
        provActual = var.ui.cmbProvprop.currentText()
        listado = conexion.Conexion().listaMuni(provActual)
        var.ui.cmbMuniprop.addItems(listado)

    def resizeTablaPropiedades(self):
        try:
            header = var.ui.tablaProp.horizontalHeader()
            for i in range(header.count()):
                if i in(1,2):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaProp.horizontalHeaderItem(i)
                if header_items is not None:
                    font = header_items.font()
                    font.setBold(True)
                    header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla prop", e)

    def abrirTipoprop(self):
        try:
            var.dlggestion.show()
        except Exception as e:
            print("error en abrir tipo prop: ", e)

    @staticmethod
    def cargarTipoprop():
        registro = conexion.Conexion.cargarTipoprop()
        var.ui.cmbTipoprop.clear()
        var.ui.cmbTipoprop.addItems(registro)

    '''
        Zona vendedores
    '''

    def cargarDelegacion(self):
        var.ui.cmbDelegVen.clear()
        listado = conexion.Conexion().listaProv(self)
        var.ui.cmbDelegVen.addItems(listado)

    def validarDNIven(dni):
        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    return True
                else:
                    return False

            else:
                return False
        except Exception as error:
            print("error en validar dni ", error)

    def resizeTablaVendedores(self):
        try:
            header = var.ui.tablaVendedores.horizontalHeader()
            for i in range(header.count()):

                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

                header_items = var.ui.tablaVendedores.horizontalHeaderItem(i)
                if header_items is not None:
                    font = header_items.font()
                    font.setBold(True)
                    header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    @staticmethod
    def resizeTablaFacturas():
        try:
            header = var.ui.tablaFacturas.horizontalHeader()
            for i in range(header.count()):
                if i != 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tablaFacturas.horizontalHeaderItem(i)
                if header_items is not None:
                    font = header_items.font()
                    font.setBold(True)
                    header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes ", e)

    @staticmethod
    def resizeTablaVentas():
        try:
            header = var.ui.tablaVentas.horizontalHeader()
            for i in range(header.count()):
                if i != 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tablaVentas.horizontalHeaderItem(i)
                if header_items is not None:
                    font = header_items.font()
                    font.setBold(True)
                    header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes ", e)