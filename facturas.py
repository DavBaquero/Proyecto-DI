import conexion
import eventos
import var
from PyQt6 import QtWidgets,QtGui, QtCore

class Facturas:

    @staticmethod
    def altaFactura():
        try:
            nuevaFactura = [var.ui.txtFechaFactura.text(),var.ui.txtdniclifac.text()]
            if var.ui.txtdniclifac.text() == "" or var.ui.txtdniclifac.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura","Recuerda seleccionar un cliente antes de grabar una factura")
            elif var.ui.txtFechaFactura.text() == "" or var.ui.txtFechaFactura.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura","No es posible grabar una factura sin seleccionar una fecha")
            elif conexion.Conexion.altaFactura(nuevaFactura):
                eventos.Eventos.crearMensajeInfo("Factura grabada", "Se ha grabado una nueva factura")
                Facturas.cargaTablaFacturas()
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido grabar factura")
        except Exception as e:
            print("factura",e)

    @staticmethod
    def cargaTablaFacturas():
        try:
            listado = conexion.Conexion.listadoFacturas()
            var.ui.tablaFacturas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))  # idFactura
                var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[1]))  # dniCliente
                var.ui.tablaFacturas.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[2]))  # fechaFactura
                var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                botondelfac = QtWidgets.QPushButton()
                botondelfac.setFixedSize(30, 24)
                botondelfac.setIcon(QtGui.QIcon('img/papelera.ico'))
                botondelfac.setProperty("row", index)
                botondelfac.clicked.connect(lambda checked, idFactura=str(registro[0]) : Facturas.eliminarFactura(idFactura))
                contenedor = QtWidgets.QWidget()
                layout = QtWidgets.QHBoxLayout()
                layout.addWidget(botondelfac)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                contenedor.setLayout(layout)
                var.ui.tablaFacturas.setCellWidget(index, 3, contenedor)
                index += 1
        except Exception as e:
            print("Error cargaFacturas en cargaTablaFacturas", e)

    @staticmethod
    def cargaOneFactura():
        try:
            fila = var.ui.tablaFacturas.currentRow()
            idFactura = var.ui.tablaFacturas.item(fila, 0).text()
            if idFactura:
                factura = conexion.Conexion.cargaOneFactura(idFactura)
                var.ui.lblNumFactura.setText(factura[0])
                var.ui.txtFechaFactura.setText(factura[1])
                var.ui.txtdniclifac.setText(factura[2])
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido cargar la factura")
            Facturas.cargarClienteVenta()
        except Exception as e:
            print("Error en cargaOneFactura",e)

    @staticmethod
    def eliminarFactura(idFactura):
        try:
            if conexion.Conexion.bajaFactura(idFactura):
                eventos.Eventos.crearMensajeInfo("Factura eliminada","Se ha eliminado la factura")
                Facturas.cargaTablaFacturas()
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido eliminar la factura")
        except Exception as e:
            print("Error en eliminarFactura",e)

    @staticmethod
    def cargarClienteVenta():
        try:
            dniCliente = var.ui.txtdniclifac.text()
            if conexion.Conexion.datosOneCliente(dniCliente):
                datosCliente = conexion.Conexion.datosOneCliente(dniCliente)
                var.ui.txtnomeclifac.setText(datosCliente[3])
                var.ui.txtapelclifac.setText(datosCliente[2])
                return True
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido cargar el cliente")
                return False
        except Exception as e:
            print("Error en cargarClienteVenta",e)

    @staticmethod
    def cargarPropiedadVenta(propiedad):
        try:
            if str(propiedad[6]).lower() == "disponible":
                var.ui.txtcodpropfac.setText(str(propiedad[1]))
                var.ui.txttipopropfac.setText(str(propiedad[2]))
                var.ui.txtpreciofac.setText(str(propiedad[3]) + " €")
                var.ui.txtdirpropfac.setText(str(propiedad[4]).title())
                var.ui.txtmunipropfac.setText(str(propiedad[5]))
                return True
            else:
                eventos.Eventos.crearMensajeError("Error","La propiedad seleccionada no está disponible")
                return False
        except Exception as e:
            print("Error en cargarPropiedadVenta", e)