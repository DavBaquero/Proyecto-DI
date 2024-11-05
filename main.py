from calendar import Calendar

import dlgGestipoprop
from venAux import *
import clientes
import conexion
import eventos
import styles
from venPrincipal import *
import sys
import var
import conexionserver

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        var.historico = 1
        var.dlgAbrir = FileDialogAbrir()
        var.dlggestion = dlg_Tipo_prop()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        # conexionserver.ConexionServer.crear_conexion()
        eventos.Eventos.cargarProvincias(self)
        eventos.Eventos.cargarProvprop(self)
        eventos.Eventos.cargarMunicipio(self)
        eventos.Eventos.cargarMuniprop(self)
        var.ui.cmbProvprop.currentIndexChanged.connect(eventos.Eventos.cargarMuniprop)
        eventos.Eventos.cargarTipoprop()
        clientes.Clientes.cargaTablaClientes(self)

        '''
        zona de eventos de las tablas
        '''
        eventos.Eventos.resizeTablaClientes(self)
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)

        propiedades.Propiedades.cargarTablaPropiedades()
        eventos.Eventos.resizeTablaPropiedades(self)
        var.ui.tablaProp.clicked.connect(propiedades.Propiedades.cargaOnePropiedad)
        '''
        zona de eventos del menubar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipo_Propiedades.triggered.connect(eventos.Eventos.abrirTipoprop)

        '''
        eventos de botones
        '''
        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,0))
        var.ui.btnBajacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,1))
        var.ui.btnAltaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1,0))
        var.ui.btnBajaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1,1))
        var.ui.btnModificli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnEliminarcli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnGrabarprop.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModifiprop.clicked.connect(propiedades.Propiedades.modifProp)
        '''
        eventos de cajas de texto
        '''
        var.ui.txtDnicli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailcli.text()))
        var.ui.txtMovilcli.editingFinished.connect(lambda: clientes.Clientes.checkMovil(var.ui.txtMovilcli.text()))
        var.ui.txtMovilprop.editingFinished.connect(lambda : propiedades.Propiedades.checkMovilProp(var.ui.txtMovilprop.text()))
        '''
        eventos combobox
        '''
        var.ui.cmbProvcli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipio)
        '''
        zona toolbar
        '''

        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpar.triggered.connect(eventos.Eventos.limpiarPanel)
        '''
        zona eventos checkbox
        '''
        var.ui.chkHistoriacli.stateChanged.connect(clientes.Clientes.historicoCli)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())