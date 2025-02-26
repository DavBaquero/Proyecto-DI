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