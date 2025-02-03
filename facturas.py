import conexion
import eventos
import propiedades
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
                var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[1]))
                var.ui.tablaFacturas.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[2]))
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
                eventos.Eventos.crearMensajeInfo("Factura eliminada", "Se ha eliminado la factura")
                Facturas.cargaTablaFacturas()
            else:
                eventos.Eventos.crearMensajeError("Error", "No se ha podido eliminar la factura")
        except Exception as e:
            print("Error en eliminarFactura", e)

    @staticmethod
    def cargarClienteVenta():
        try:
            dniCliente = var.ui.txtdniclifac.text()
            if conexion.Conexion.datosOneCliente(dniCliente):
                datosCliente = conexion.Conexion.datosOneCliente(dniCliente)
                var.ui.txtnomeclifac.setText(datosCliente[3])
                var.ui.txtapelclifac.setText(datosCliente[2])
                Facturas.cargaTablaVentas()
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

    @staticmethod
    def altaVenta():
        try:
            nuevaVenta = [var.ui.lblNumFactura.text(), var.ui.txtcodpropfac.text(), var.ui.txtidvenfac.text()]
            if var.ui.txtcodpropfac.text() == "" or var.ui.txtcodpropfac.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar venta","Recuerda seleccionar una propiedad antes de grabar una venta")
            elif var.ui.txtidvenfac.text() == "" or var.ui.txtidvenfac.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar venta","Recuerda seleccionar un vendedor antes de grabar una venta")
            elif conexion.Conexion.altaVenta(nuevaVenta) and conexion.Conexion.actualizaPropiedadVenta(nuevaVenta[1]):
                eventos.Eventos.crearMensajeInfo("Venta grabada", "Se ha grabado una nueva venta")
                Facturas.cargaTablaVentas()
                propiedades.Propiedades.cargarTablaPropiedades()
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido grabar venta")
        except Exception as e:
            print("venta",e)


    @staticmethod
    def cargaTablaVentas():
        idFactura = var.ui.lblNumFactura.text()
        listado = conexion.Conexion.listadoVentas(idFactura)
        var.ui.tablaVentas.setRowCount(len(listado))
        index = 0
        subtotal = 0
        for registro in listado:
            var.ui.tablaVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
            var.ui.tablaVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
            var.ui.tablaVentas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
            var.ui.tablaVentas.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[3])))
            var.ui.tablaVentas.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[4])))
            var.ui.tablaVentas.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[5]) + " € "))

            botondelfac = QtWidgets.QPushButton()
            botondelfac.setFixedSize(30, 24)
            botondelfac.setIcon(QtGui.QIcon('img/papelera.ico'))
            botondelfac.setProperty("row", index)
            botondelfac.clicked.connect(lambda checked, idVenta=str(registro[0]), idpropiedad=str(registro[1]): Facturas.eliminarVenta(idVenta, idpropiedad))
            contenedor = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(botondelfac)
            layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            contenedor.setLayout(layout)
            var.ui.tablaVentas.setCellWidget(index, 6, contenedor)
            if var.ui.tablaVentas.item(index, 0):
                var.ui.tablaVentas.item(index, 0).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 1):
                var.ui.tablaVentas.item(index, 1).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 2):
                var.ui.tablaVentas.item(index, 2).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 3):
                var.ui.tablaVentas.item(index, 3).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 4):
                var.ui.tablaVentas.item(index, 4).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 5):
                var.ui.tablaVentas.item(index, 5).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            subtotal += registro[5]


            index += 1

        iva = subtotal * 0.21
        total = subtotal + iva
        subTotalStr = f"{subtotal:,.1f} €"
        ivaStr = f"{iva:,.1f} €"
        totalStr = f"{total:,.1f} €"
        var.ui.lblSubtotalFactura.setText(subTotalStr)
        var.ui.lblImpuestasFacturas.setText(ivaStr)
        var.ui.lblTotalFactura.setText(totalStr)

    @staticmethod
    def cargaOneVenta():
        try:
            fila = var.ui.tablaVentas.currentRow()
            idVenta = var.ui.tablaVentas.item(fila, 0).text()
            print("idVenta",idVenta)
            if idVenta:
                venta = conexion.Conexion.datosOneVenta(idVenta)
                print(venta)
                var.ui.txtidvenfac.setText(venta[0])
                var.ui.txtcodpropfac.setText(str(venta[1]))
                var.ui.txttipopropfac.setText(venta[2])
                var.ui.txtpreciofac.setText(str(venta[3]) + " € ")
                var.ui.txtmunipropfac.setText(venta[4])
                var.ui.txtdirpropfac.setText(venta[5])
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido cargar la venta")
        except Exception as e:
            print("Error en cargaOneVenta",e)

    def eliminarVenta(idVenta, idpropiedad):
        try:
            if conexion.Conexion.bajaVenta(idVenta) and conexion.Conexion.altaPropiedadVenta(str(idpropiedad)):
                eventos.Eventos.crearMensajeInfo("Venta eliminada","Se ha eliminado la venta")
                Facturas.cargaTablaVentas()
                propiedades.Propiedades.cargarTablaPropiedades()
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido eliminar la venta")
        except Exception as e:
            print("Error en eliminarVenta",e)