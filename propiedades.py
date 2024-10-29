import conexion
import var


class Propiedades():
    def altaTipopropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            registro = conexion.Conexion.altaTipoprop(tipo)
            var.ui.cmbTipoprop.clear()
            var.ui.cmbTipoprop.addItems(registro)
        except Exception as e:
            print(f"Error: {e}")


    def bajaTipopropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            print(tipo)
        except Exception as e:
            print(f"Error: {e}")

    def altaPropiedad(self):
        try:
            propiedad = [var.ui.txtAltaprop.text(),var.ui.txtDirprop.text(),var.ui.cmbProvprop.currentText(),
                         var.ui.cmbMuniprop.currentText(),var.ui.txtCpprop.text(),var.ui.cmbTipoprop.currentText(),
                         var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),
                         var.ui.txtPrecioVentaprop.text(), var.ui.txtPrecioAlquilerprop.text(),var.ui.areatxtDescriprop.toPlainText(),
                         var.ui.txtNomeprop.text(),var.ui.txtMovilprop.text()]
            print(propiedad)
        except Exception as e:
            print(str(e))