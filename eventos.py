import os
import sys
from PyQt6 import QtWidgets, QtGui

import alquileres
import conexion
import facturas
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Mensaje de salida de la aplicación

        """
        mbox = Eventos.crearMensajeSalida('Salir',"¿Desea salir?")
        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    @staticmethod
    def crearMensajeSalida(titulo_ventana, mensaje):
        """
        :param titulo_ventana: Título de la ventana
        :type titulo_ventana: String
        :param mensaje: Mensaje a mostrar
        :type mensaje: String
        :return: Mensaje de salida
        :rtype: QtWidgets.QMessageBox

        Metodo que crea un mensaje de salida de la aplicación
        """
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
        """

        :param titulo_ventana: Título de la ventana
        :type titulo_ventana: String
        :param mensaje: Mensaje a mostrar
        :type mensaje: String
        :return: Mensaje de información
        :rtype: QtWidgets.QMessageBox

        Metodo que crea un mensaje de información

        """
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
        """

        :param titulo_ventana: Título de la ventana
        :type titulo_ventana: String
        :param mensaje: Mensaje a mostrar
        :type mensaje: String
        :return: Mensaje de error
        :rtype: QtWidgets.QMessageBox

        Metodo que crea un mensaje de error

        """
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
        """
        :param pan: Indica el panel
        :type pan: int
        :param btn: Indica el botón
        :type btn: int

        Metodo que abre el calendario

        """
        try:
            var.panel = pan
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    def cargarFecha(qDate):
        """
        :param qDate: Fecha seleccionada
        :type qDate: Date
        :return: Fecha seleccionada
        :rtype: date

        Metodo que carga la fecha seleccionada en el calendario

        """
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
            elif var.panel == 4 and var.btn == 0:
                var.ui.txtfechainicioalq.setText(str(data))
            elif var.panel == 4 and var.btn == 1:
                var.ui.txtfechafinalq.setText(str(data))

            time.sleep(0.125)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def crearBackup(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que crea una copia de seguridad de la base de datos

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que restaura una copia de seguridad de la base de datos

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que limpia los campos del panel seleccionado
        """
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
                facturas.Facturas.cargaTablaVentas()
            elif current_index == 4:
                alquiler = [var.ui.lblnumalq, var.ui.txtfechainicioalq, var.ui.txtfechafinalq, var.ui.txtnomeclialq,
                              var.ui.txtapelclialq, var.ui.txtdniclialq, var.ui.txtidvenalq, var.ui.txtcodpropalq,
                              var.ui.txttipopropalq, var.ui.txtprecioalq, var.ui.txtmunipropalq, var.ui.txtdirpropalq]
                for i, dato in enumerate(alquiler):
                    if i != 2 or i !=3:
                        dato.setText("")
                    else:
                        dato.setText(datetime.today().strftime('%d/%m/%Y'))
                alquileres.Alquileres.cargarTablaMensualidad(-1)
            else:
                print("panPrincipal es nulo")
        except Exception as e:
            print(f"Se ha producido una excepción: {e}")

    def abrirAbout(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que abre la ventana de acerca de

        """
        try:
            var.dlgabout.show()
        except Exception as e:
            print("error en abrir about: ", e)

    def cerrarAcercaDe(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que cierra la ventana de acerca de

        """
        try:
            var.dlgabout.close()
        except Exception as e:
            print("error en cerrar acerca de: ", e)

    def filtrar(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que filtra los registros de la tabla seleccionada

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que carga las provincias en el combo box de provincias

        """
        var.ui.cmbProvcli.clear()
        listado = conexion.Conexion().listaProv(self)
        # listado = conexionserver.ConexionServer.listaProv()
        var.ui.cmbProvcli.addItems(listado)

    def cargarMunicipio(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que carga los municipios en el combo box de municipios según la provincia seleccionada

        """
        var.ui.cmbMunicli.clear()
        provActual = var.ui.cmbProvcli.currentText()
        listado = conexion.Conexion().listaMuni(provActual)
        # listado = conexionserver.ConexionServer.listaProv()
        var.ui.cmbMunicli.addItems(listado)

    def validarDNIcli(dni):
        """
        :param dni: DNI a validar
        :type dni: String
        :return: True si el DNI es válido, False si no lo es
        :rtype: Boolean

        Metodo que valida un DNI

        """
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
        """
        :param mail: Mail a validar
        :type mail: String
        :return: True si el mail es válido, False si no lo es
        :rtype: Boolean

        Metodo que valida un mail

        """
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, mail) or mail == '':
            return True
        else:
            return False

    def validarMovil(movil):
        """
        :param movil: Móvil a validar
        :type movil: String
        :return: True si el móvil es válido, False si no lo es
        :rtype: Boolean

        Metodo que valida un móvil

        """
        regex = r'^(6\d{8}|7\d{8})$'
        if (re.match(regex, movil) and len(movil) == 9) or (movil == ''):
            return True
        else:
            return False

    def resizeTablaClientes(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que redimensiona la tabla de clientes

        """
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
        """
        :return: None
        :rtype: None

        Metodo que abre la ventana para generar un informe de propiedades según municipio

        """
        try:
            var.dlgInformeProp.show()
        except Exception as e:
            print("error en abrir informe propiedades: ", e)

    def cargarProvprop(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que carga las provincias en el combo box de provincias de propiedades

        """
        var.ui.cmbProvprop.clear()
        listado = conexion.Conexion().listaProv(self)
        var.ui.cmbProvprop.addItems(listado)

    def cargarMuniprop(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que carga los municipios en el combo box de municipios de propiedades según la provincia seleccionada
        """
        var.ui.cmbMuniprop.clear()
        provActual = var.ui.cmbProvprop.currentText()
        listado = conexion.Conexion().listaMuni(provActual)
        var.ui.cmbMuniprop.addItems(listado)

    def resizeTablaPropiedades(self):
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que redimensiona la tabla de propiedades

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que abre la ventana de gestión de tipos de propiedades

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que carga las delegaciones en el combo box de delegaciones

        """
        var.ui.cmbDelegVen.clear()
        listado = conexion.Conexion().listaProv(self)
        var.ui.cmbDelegVen.addItems(listado)

    def validarDNIven(dni):
        """
        :param dni: DNI a validar
        :type dni: String
        :return: True si el DNI es válido, False si no lo es
        :rtype: Boolean

        Metodo que valida un DNI

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que redimensiona la tabla de vendedores

        """
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
        """

        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que redimensiona la tabla de facturas

        """
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
        """
        :param self: None
        :type self: None
        :return: None
        :rtype: None

        Metodo que redimensiona la tabla de ventas

        """
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

    @staticmethod
    def resizeTablaContratos():
        header = var.ui.tablacontratosalq.horizontalHeader()
        for i in range(header.count()):
            if i != 0:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header_items = var.ui.tablacontratosalq.horizontalHeaderItem(i)
            if header_items is not None:
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)


    @staticmethod
    def resizeTablaMensualidad():
        header = var.ui.tablaMensualidades.horizontalHeader()
        for i in range(header.count()):
            if i != 0:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header_items = var.ui.tablaMensualidades.horizontalHeaderItem(i)
            if header_items is not None:
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)