import conexion
import eventos
import propiedades
import var
from PyQt6 import QtWidgets,QtGui, QtCore


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
            else:
                conexion.Conexion.altaAlquiler(nuevoAlquiler)
                conexion.Conexion.actualizaPropiedadAlquiler(nuevoAlquiler[0])
                mbox = eventos.Eventos.crearMensajeInfo("Alta alquiler","Alquiler dado de alta correctamente")
                mbox.exec()
                propiedades.Propiedades.cargarTablaPropiedades()
                #eventos.Eventos.cargarTablaAlquiler()
        except Exception as e:
            mbox = eventos.Eventos.crearMensajeError("Error alta alquiler","Error al dar alta alquiler")
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
                index += 1
        except Exception as e:
            print("Error cargaFacturas en cargaTablaFacturas", e)


    @staticmethod
    def cargarOneContrato():
        try:
            var.ui.btnCrearContrato.setDisabled(True)
            fila = var.ui.tablacontratosalq.currentRow()
            idAlquiler = var.ui.tablacontratosalq.item(fila, 0).text()

            if idAlquiler:
                alquiler = conexion.Conexion.cargaOneContrato(idAlquiler)
                print(alquiler)
                var.ui.lblnumalq.setText(alquiler[0])
                var.ui.txtfechainicioalq.setText(alquiler[1])
                var.ui.txtfechafinalq.setText(alquiler[2])
            else:
                mbox = eventos.Eventos.crearMensajeError("Error cargar contrato",
                                                         "Error al intentar cargar un contrato")
                mbox.exec()
        except Exception as e:
            print("Error carga alquiler: ", e)