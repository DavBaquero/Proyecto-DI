import eventos
import var


class Alquileres:

    @staticmethod
    def altaAlquiler():
        try:
            nuevoAlquiler =[var.ui.txtcodpropalq.text(), var.ui.txtdniclialq.text(), var.ui.txtfechainicioalq.text(),
                            var.ui.txtfechafinalq.text(), var.ui.txtidvenalq.text()]
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