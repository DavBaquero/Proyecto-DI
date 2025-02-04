from calendar import Calendar
from xmlrpc.client import DateTime

import facturas
import informes
import vendedores
from venAux import *
import clientes
import conexion
import eventos
import styles
from venPrincipal import *
import sys
import var

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        '''
            zona de inicializar de las tablas
        '''
        conexion.Conexion.db_conexion(self)
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        var.historicocli = 1
        var.historicoprop = 1
        var.current_page_cli = 0
        var.items_per_page_cli = 20
        var.current_page_prop = 0
        var.items_per_page_prop = 16
        var.dlgAbrir = FileDialogAbrir()
        var.dlggestion = dlg_Tipo_prop()
        var.dlgInformeProp = Dlg_InformeProp()
        var.dlgabout = dlg_About()
        self.setStyleSheet(styles.load_stylesheet())
        # conexionserver.ConexionServer.crear_conexion()

        '''
            zona de inicializar eventos
        '''
        eventos.Eventos.cargarProvincias(self)
        eventos.Eventos.cargarMunicipio(self)

        eventos.Eventos.cargarProvprop(self)
        eventos.Eventos.cargarMuniprop(self)
        eventos.Eventos.cargarTipoprop()
        eventos.Eventos.cargarDelegacion(self)

        '''
        zona de eventos de las tablas
        '''
        clientes.Clientes.cargaTablaClientes(self)
        propiedades.Propiedades.cargarTablaPropiedades()
        vendedores.Vendedores.cargaTablaVendedores(self)
        facturas.Facturas.cargaTablaFacturas()
        facturas.Facturas.cargaTablaVentas()

        eventos.Eventos.resizeTablaClientes(self)
        eventos.Eventos.resizeTablaPropiedades(self)
        eventos.Eventos.resizeTablaVendedores(self)
        eventos.Eventos.resizeTablaFacturas()
        eventos.Eventos.resizeTablaVentas()

        var.ui.tablaProp.clicked.connect(propiedades.Propiedades.cargaOnePropiedad)
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)
        var.ui.tablaFacturas.clicked.connect(facturas.Facturas.cargaOneFactura)
        var.ui.tablaVendedores.clicked.connect(vendedores.Vendedores.cargaOneVendedor)
        var.ui.tablaVentas.clicked.connect(facturas.Facturas.cargaOneVenta)

        '''
        zona de eventos del menubar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipo_Propiedades.triggered.connect(eventos.Eventos.abrirTipoprop)
        var.ui.actionAcerca_de.triggered.connect(eventos.Eventos.abrirAbout)

        '''
        eventos de botones
        '''
        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnModificli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnEliminarcli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,0))
        var.ui.btnBajacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,1))

        var.ui.btnAltaVen.clicked.connect(lambda: eventos.Eventos.abrirCalendar(2,0))
        var.ui.btnBajaVen.clicked.connect(lambda: eventos.Eventos.abrirCalendar(2,1))
        var.ui.btnGrabarVen.clicked.connect(vendedores.Vendedores.altaVendedores)
        var.ui.btnModifiVen.clicked.connect(vendedores.Vendedores.modifVen)
        var.ui.btnEliminarVen.clicked.connect(vendedores.Vendedores.bajaVendedor)



        var.ui.btnEliminarprop.clicked.connect(propiedades.Propiedades.bajaProp)
        var.ui.btnGrabarprop.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModifiprop.clicked.connect(propiedades.Propiedades.modifProp)
        var.ui.btnAltaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1, 0))
        var.ui.btnBajaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1, 1))
        var.ui.btnBuscProp.clicked.connect(propiedades.Propiedades.filtrarPropiedades)
        var.ui.btnFiltrarCli.clicked.connect(clientes.Clientes.filtrar)
        var.ui.btnFechaFactura.clicked.connect(lambda: eventos.Eventos.abrirCalendar(3,0))
        var.ui.btnGrabarFactura.clicked.connect(facturas.Facturas.altaFactura)
        var.ui.btnGrabarVenta.clicked.connect(facturas.Facturas.altaVenta)

        var.ui.btnAntCli.clicked.connect(clientes.Clientes.anteriorCliente)
        var.ui.btnAntProp.clicked.connect(propiedades.Propiedades.anteriorPropiedad)

        var.ui.btnSigCli.clicked.connect(clientes.Clientes.siguienteCliente)
        var.ui.btnSigProp.clicked.connect(propiedades.Propiedades.siguientePropiedad)

        var.ui.btnIformeFac.clicked.connect(lambda: informes.Informes.reportFact(var.ui.lblNumFactura.text()))

        '''
        eventos de cajas de texto
        '''
        var.ui.txtDnicli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDnicli.text()))
        var.ui.txtDNIVen.editingFinished.connect(lambda: vendedores.Vendedores.checkDNIven(var.ui.txtDNIVen.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailcli.text()))
        var.ui.txtMailVen.editingFinished.connect(lambda: vendedores.Vendedores.checkEmailven(var.ui.txtMailVen.text()))
        var.ui.txtMovilcli.editingFinished.connect(lambda: clientes.Clientes.checkMovil(var.ui.txtMovilcli.text()))
        var.ui.txtMovilVen.editingFinished.connect(lambda: vendedores.Vendedores.checkMovilven(var.ui.txtMovilVen.text()))
        var.ui.txtBajaprop.textChanged.connect(lambda: propiedades.Propiedades.manageRadioButtons())
        var.ui.txtPrecioVentaprop.textChanged.connect(lambda: propiedades.Propiedades.manageChkBox())
        var.ui.txtPrecioAlquilerprop.textChanged.connect(lambda: propiedades.Propiedades.manageChkBox())
        var.ui.txtMovilprop.editingFinished.connect(lambda : propiedades.Propiedades.checkMovilProp(var.ui.txtMovilprop.text()))
        var.ui.txtFechaFactura.setText(datetime.today().strftime('%d/%m/%Y'))
        '''
        eventos combobox
        '''

        var.ui.cmbProvcli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipio)
        var.ui.cmbTipoprop.currentIndexChanged.connect(propiedades.Propiedades.cargarTablaPropiedades)
        var.ui.cmbProvprop.currentIndexChanged.connect(eventos.Eventos.cargarMuniprop)
        var.ui.actionbarFiltrar.triggered.connect(eventos.Eventos.filtrar)
        var.ui.actionExportar_Propiedades_CSV.triggered.connect(propiedades.Propiedades.exportarCSVProp)
        var.ui.actionExprotar_Propiedades_JSON.triggered.connect(propiedades.Propiedades.exportarJSONProp)
        var.ui.actionExportar_Clientes_CSV.triggered.connect(clientes.Clientes.exportarCSVCli)
        var.ui.actionExportar_Clientes_JSON.triggered.connect(clientes.Clientes.exportarJSONCli)
        var.ui.actionListado_clientes.triggered.connect(informes.Informes.reportClientes)
        var.ui.actionListado_propiedades.triggered.connect(eventos.Eventos.abrir_informeProp)
        '''
        zona toolbar
        '''
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpar.triggered.connect(eventos.Eventos.limpiarPanel)

        '''
        zona eventos checkbox
        '''
        var.ui.chkHistoriacli.stateChanged.connect(clientes.Clientes.historicoCli)
        propiedades.Propiedades.manageRadioButtons()
        var.ui.chkHistoriaprop.stateChanged.connect(propiedades.Propiedades.historicoProp)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())