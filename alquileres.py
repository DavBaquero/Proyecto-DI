import datetime

from PyQt6.QtWidgets import QHBoxLayout, QWidget

import conexion
import eventos
import informes
import propiedades
import var
from PyQt6 import QtWidgets,QtGui, QtCore
from dateutil.relativedelta import relativedelta



class Alquileres:

    @staticmethod
    def altaAlquiler():
        try:
            nuevoAlquiler =[var.ui.txtcodpropalq.text(), var.ui.txtdniclialq.text(), var.ui.txtfechainicioalq.text(),
                            var.ui.txtfechafinalq.text(), var.ui.txtidvenalq.text()]
            if nuevoAlquiler[0] == "":
                mbox = eventos.Eventos.crearMensajeError("Error alta alquiler","Debe seleccionar una propiedad")
                mbox.exec()
            elif nuevoAlquiler[1] == "":
                mbox = eventos.Eventos.crearMensajeError("Error alta alquiler","Debe seleccionar un cliente")
                mbox.exec()
            elif nuevoAlquiler[4] == "":
                mbox = eventos.Eventos.crearMensajeError("Error alta alquiler","Debe seleccionar un vendedor")
                mbox.exec()
            elif ((conexion.Conexion.altaAlquiler(nuevoAlquiler)) and
                (conexion.Conexion.actualizaPropiedadAlquiler(nuevoAlquiler[0])) and Alquileres.generaMensualidad(nuevoAlquiler)):

                mbox = eventos.Eventos.crearMensajeInfo("Alta alquiler","Alquiler dado de alta correctamente")
                mbox.exec()
                propiedades.Propiedades.cargarTablaPropiedades()
                Alquileres.cargarTablaContratos()
        except Exception as e:
            mbox = eventos.Eventos.crearMensajeError("Error alta alquiler","Error al dar alta alquiler")
            mbox.exec()
            print("Error al dar de alta un alquiler", e)


    @staticmethod
    def cargarPropiedadAlquiler(propiedad):
        try:
            if str(propiedad[6]).lower() == "disponible":
                var.ui.txtcodpropalq.setText(str(propiedad[1]))
                var.ui.txttipopropalq.setText(str(propiedad[2]))
                var.ui.txtprecioalq.setText(str(propiedad[3]) + " €")
                var.ui.txtdirpropalq.setText(str(propiedad[4]).title())
                var.ui.txtmunipropalq.setText(str(propiedad[5]))
                return True
            else:
                mbox = eventos.Eventos.crearMensajeError("Error","La propiedad seleccionada no está disponible")
                mbox.exec()
                return False
        except Exception as e:
            print("Error en cargarPropiedadVenta", e)


    @staticmethod
    def cargarTablaContratos():
        try:
            listado = conexion.Conexion.listadoContrato()
            var.ui.tablacontratosalq.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablacontratosalq.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablacontratosalq.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[1]))
                var.ui.tablacontratosalq.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablacontratosalq.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                botonEliminar = QtWidgets.QPushButton()
                botonEliminar.setFixedSize(25, 25)
                botonEliminar.setIconSize(QtCore.QSize(25, 25))
                botonEliminar.setObjectName("botonEliminarCont")
                botonEliminar.setIcon(QtGui.QIcon('./img/papelera.ico'))

                # creamos layout para centrar el boton
                layout = QHBoxLayout()
                layout.addWidget(botonEliminar)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)

                # Crear un widget contenedor para el layout y agregarlo a la celda
                container = QWidget()
                container.setLayout(layout)
                var.ui.tablacontratosalq.setCellWidget(index, 2, container)
                botonEliminar.clicked.connect(
                    lambda checked, idAlquiler=registro[0],: Alquileres.eliminarAlquiler(idAlquiler))
                index += 1
        except Exception as e:
            print("Error cargaFacturas en cargaTablaFacturas", e)


    @staticmethod
    def cargarOneContrato():
        try:
            var.ui.btnCrearContrato.setDisabled(True)
            fila = var.ui.tablacontratosalq.currentRow()
            idAlquiler = var.ui.tablacontratosalq.item(fila, 0).text()
            listado = [var.ui.lblnumalq,var.ui.txtfechainicioalq, var.ui.txtfechafinalq, var.ui.txtidvenalq,
                       var.ui.txtdniclialq, var.ui.txtnomeclialq, var.ui.txtapelclialq, var.ui.txtcodpropalq,
                       var.ui.txttipopropalq, var.ui.txtprecioalq, var.ui.txtmunipropalq, var.ui.txtdirpropalq]

            if idAlquiler:
                alquiler = conexion.Conexion.datosOneAlquiler(idAlquiler)
                for i, dato in enumerate(alquiler):
                    listado[i].setText(str(dato))
                Alquileres.cargarTablaMensualidad(idAlquiler)

            else:
                mbox = eventos.Eventos.crearMensajeError("Error cargar contrato",
                                                         "Error al intentar cargar un contrato")
                mbox.exec()
        except Exception as e:
            print("Error carga alquiler: ", e)


    @staticmethod
    def generaMensualidad(registro):
        try:
            fechaIniciostr = registro[2]
            fechaFinalstr = registro[3]
            propiedad = registro[0]
            cliente = registro[1]
            idAlquiler = conexion.Conexion.buscarAlquiler(propiedad,cliente)


            fechaInicio = datetime.datetime.strptime(fechaIniciostr, "%d/%m/%Y")
            fechaFinal = datetime.datetime.strptime(fechaFinalstr, "%d/%m/%Y")

            while fechaInicio.year <= fechaFinal.year and (
                    fechaInicio.year < fechaFinal.year or fechaInicio.month <= fechaFinal.month):
                mes = fechaInicio.strftime("%B").capitalize()
                mes_anio = f"{mes} {fechaInicio.year}"
                registro = [idAlquiler, mes_anio, 0]
                if not conexion.Conexion.altaMensualidad(registro):
                    return False
                fechaInicio += relativedelta(months=1)

            return True

        except ValueError as e:
            print("Error: Las fechas no tienen el formato correcto o no son válidas.", e)
            return False

        except TypeError as e:
            print("Error: Se esperaba una cadena de texto para la fecha.", e)
            return False


    @staticmethod
    def cargarTablaMensualidad(idAlquiler):
        try:
            listado = conexion.Conexion.listadoMensualidad(idAlquiler)
            var.ui.tablaMensualidades.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablaMensualidades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaMensualidades.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tablaMensualidades.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tablaMensualidades.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[3])))

                checkbox = QtWidgets.QCheckBox()
                checkbox.setChecked(bool(int(registro[4])))

                checkboxLayout = QHBoxLayout()
                checkboxLayout.addWidget(checkbox)
                checkboxLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                checkboxLayout.setContentsMargins(0, 0, 0, 0)
                checkboxLayout.setSpacing(0)

                checkboxContainer = QWidget()
                checkboxContainer.setLayout(checkboxLayout)
                var.ui.tablaMensualidades.setCellWidget(index, 4, checkboxContainer)
                checkbox.clicked.connect(lambda checked, idMensualidad=registro[0]: Alquileres.pagarMensualidad(idMensualidad))

                botonInfor = QtWidgets.QPushButton()
                botonInfor.setStyleSheet("background-color: #f5f5f5;")
                botonInfor.setFixedSize(20, 20)
                botonInfor.setIconSize(QtCore.QSize(20, 20))
                botonInfor.setIcon(QtGui.QIcon('./img/informe.ico'))

                layoutBoton = QHBoxLayout()
                layoutBoton.addWidget(botonInfor)
                layoutBoton.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layoutBoton.setContentsMargins(0, 0, 0, 0)
                layoutBoton.setSpacing(0)

                containerBoton = QWidget()
                containerBoton.setLayout(layoutBoton)
                var.ui.tablaMensualidades.setCellWidget(index, 5, containerBoton)
                botonInfor.clicked.connect(lambda checked, idMensualidad=registro[0],
                                                        idAlquilerInforme=idAlquiler:
                                           informes.Informes.reportReciboMensualidad(idAlquilerInforme, idMensualidad))

                var.ui.tablaMensualidades.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaMensualidades.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1
        except Exception as e:
            print("Error cargaFacturas en cargaTablaFacturas", e)

    @staticmethod
    def pagarMensualidad(idMensualidad):
        try:
            if conexion.Conexion.pagarMensualidad(idMensualidad):
                if conexion.Conexion.estadoPago(idMensualidad) == 0:
                    mbox = eventos.Eventos.crearMensajeInfo("Pago mensualidad","Pago revertido correctamente")
                elif conexion.Conexion.estadoPago(idMensualidad) == 1:
                    mbox = eventos.Eventos.crearMensajeInfo("Pago mensualidad","Mensualidad pagada correctamente")
                mbox.exec()
            else:
                mbox = eventos.Eventos.crearMensajeError("Error pago mensualidad","Error al pagar mensualidad")
                mbox.exec()
        except Exception as e:
            print("Error al pagar meses", e)
            return False

    @staticmethod
    def modificarContrato():
        try:
            registro = [var.ui.txtcodpropalq.text(), var.ui.txtdniclialq.text(), var.ui.txtfechainicioalq.text(),
                        var.ui.txtfechafinalq.text(), var.ui.txtidvenalq.text()]
            nuevaFecha = registro[3]
            idContrato = var.ui.lblnumalq.text()

            datosContrato = conexion.Conexion.datosOneAlquiler(idContrato)
            fechaFin = datosContrato[2]

            nuevaFechaFin = datetime.datetime.strptime(str(nuevaFecha), "%d/%m/%Y")
            fechaFinRegistrada = datetime.datetime.strptime(fechaFin, "%d/%m/%Y")

            if nuevaFechaFin == fechaFinRegistrada:
                mbox = eventos.Eventos.crearMensajeError("Error",
                                                  "La nueva fecha de fin de contrato es la misma que está registrada. No se ha modificado el contrato.")
                mbox.exec()
            elif nuevaFechaFin > fechaFinRegistrada:
                registro[2] = fechaFinRegistrada
                if Alquileres.ampliarMensualidades(idContrato, fechaFinRegistrada, nuevaFechaFin):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso", "Se han añadido nuevas mensualidades.")
                    mbox.exec()
                    Alquileres.cargarTablaMensualidad(idContrato)
            elif nuevaFechaFin < fechaFinRegistrada:
                if Alquileres.eliminarMensualidad(idContrato, nuevaFechaFin):
                    mbox = eventos.Eventos.crearMensajeInfo("Aviso",
                                                     "Se ha recortado el contrato correctamente.")
                    mbox.exec()
                    Alquileres.cargarTablaMensualidad(idContrato)
                else:
                    mbox =eventos.Eventos.crearMensajeError("Atención",
                                                      "Es posible que haya meses que no se han eliminado al detectarse pagos en el contrato. Es posible que se haya producido un error.")
                    mbox.exec()
                    Alquileres.cargarTablaMensualidad(idContrato)
            else:
                mbox =eventos.Eventos.crearMensajeError("Error", "Se ha producido un error inesperado.")
                mbox.exec()
        except Exception as e:
            print("Error al modificar contrato: ", e)

    @staticmethod
    def ampliarMensualidades(idAlquiler, fechaInicio, nuevaFecha):
        try:

            fechaInicio += relativedelta(months=+1)

            while fechaInicio.year <= nuevaFecha.year and (
                    fechaInicio.year < nuevaFecha.year or fechaInicio.month <= nuevaFecha.month):
                mes = fechaInicio.strftime("%B").capitalize()
                mes_anio = f"{mes} {fechaInicio.year}"
                registro = [idAlquiler, mes_anio, 0]
                if not conexion.Conexion.altaMensualidad(registro):
                    return False
                fechaInicio += relativedelta(months=1)

            nuevaFecha = nuevaFecha.strftime("%d/%m/%Y")
            conexion.Conexion.modificarFechaContrato(idAlquiler, nuevaFecha)
            return True

        except ValueError as e:
            print("Error: Las fechas no tienen el formato correcto o no son válidas.", e)
            return False
        except TypeError as e:
            print("Error: Se esperaba una cadena de texto para la fecha.", e)
            return False

    @staticmethod
    def eliminarMensualidad(idAlquiler, nuevaFecha):
        try:

            mensualidad = conexion.Conexion.listadoMensualidad(idAlquiler)
            for i in range(len(mensualidad) - 1, -1, -1):
                idMensualidad = mensualidad[i][0]
                mesStr = mensualidad[i][2]
                mes = datetime.datetime.strptime(str(mesStr), "%B %Y")
                pagado = mensualidad[i][4]

                if nuevaFecha < mes and not pagado:
                    conexion.Conexion.eliminarMensualidad(idMensualidad)
                elif nuevaFecha > mes:
                    break;
                elif pagado:
                    return False

            nuevaFecha = nuevaFecha.strftime("%d/%m/%Y")
            conexion.Conexion.modificarFechaContrato(idAlquiler, nuevaFecha)
            return True
        except Exception as e:
            print("Error eliminando mensualidades en alquileres", str(e))

    @staticmethod
    def eliminarAlquiler(idAlquiler):
        try:
            codProp = var.ui.txtcodpropalq.text()
            hasMensualidadesPagadas = False
            mensualidades = conexion.Conexion.listadoMensualidad(idAlquiler)
            for mensualidad in mensualidades:
                isPagado = mensualidad[4]
                if isPagado:
                    hasMensualidadesPagadas = True
                    break

            mbox = eventos.Eventos.crearMensajeConfirmacion('Eliminar contrato',
                                                            "¿Desea eliminar el contrato de alquiler seleccionado? Tenga en cuenta que la acción es irreversible.")
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                if hasMensualidadesPagadas:
                    Alquileres.eliminarMensualidad(idAlquiler, datetime.datetime.now())
                    fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y")
                    conexion.Conexion.finalizarContrato(idAlquiler, codProp, fecha_hoy)
                    Alquileres.cargarTablaMensualidad(idAlquiler)
                    eventos.Eventos.crearMensajeInfo("Aviso",
                                                     "Se han eliminado las mensualidades pendientes. El contrato no se puede eliminar, ya existen mensualidades pagadas.")
                elif not hasMensualidadesPagadas and conexion.Conexion.eliminarContratoAlquiler(idAlquiler):
                    eventos.Eventos.crearMensajeInfo("Aviso", "Se ha eliminado el contrato de alquiler.")
                    Alquileres.cargarTablaContratos()
                    Alquileres.cargarTablaMensualidad(0)
                else:
                    eventos.Eventos.crearMensajeError("Error",
                                                      "Se ha producido un error y no se ha eliminado el contrato de alquiler.")

        except Exception as e:
            print("Error al eliminar un alquiler en alquileres", str(e))