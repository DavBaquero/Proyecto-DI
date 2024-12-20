import os
from datetime import datetime

from PyQt6 import QtSql, QtWidgets, QtGui,QtCore

import eventos
import var


class Conexion:

    '''

    método de una clase que no depende de una instancia específica de esa clase. 
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase. 
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.
    
    '''

    @staticmethod
    def db_conexion(self):
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                               QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False


    @staticmethod
    def listaProv(self):
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def listaMuni(provincia):

        listamunicipios = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = ?)")
        query.bindValue(0, provincia)

        if query.exec():
            while query.next():
                listamunicipios.append(query.value(1))
        return listamunicipios

    def altaCliente(nuevocli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO CLIENTES(dnicli, altacli, apelcli, nomecli, emailcli, "
                          "movilcli, dircli, provcli, municli, bajacli) VALUES (:dnicli, :altacli, :apelcli, :nomecli, "
                          ":emailcli, :movilcli, :dircli, :provcli, :municli, :bajacli)")
            query.bindValue(":dnicli", str(nuevocli[0]))
            query.bindValue(":altacli", str(nuevocli[1]))
            query.bindValue(":apelcli", str(nuevocli[2]))
            query.bindValue(":nomecli", str(nuevocli[3]))
            query.bindValue(":emailcli", str(nuevocli[4]))
            query.bindValue(":movilcli", str(nuevocli[5]))
            query.bindValue(":dircli", str(nuevocli[6]))
            query.bindValue(":provcli", str(nuevocli[7]))
            query.bindValue(":municli", str(nuevocli[8]))
            query.bindValue(":bajacli", str(nuevocli[9]))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error en alta cliente ", e)

    @staticmethod
    def listadoClientes():
        try:
            listado = []
            historico = var.ui.chkHistoriacli.isChecked()
            filtrado = var.ui.btnFiltrarCli.isChecked()
            dni = var.ui.txtDnicli.text()
            query = QtSql.QSqlQuery()
            if not historico and filtrado:
                query.prepare("SELECT * FROM clientes where bajacli is null and dnicli = :dnicli or bajacli is not null and dnicli = :dnicli ORDER BY apelcli, nomecli ASC ")
                query.bindValue(":dnicli", dni)

            elif historico and not filtrado:
                query.prepare("SELECT * FROM clientes where bajacli is NULL or bajacli is not null ORDER BY apelcli, nomecli ASC ")

            elif historico and filtrado:
                query.prepare("SELECT * FROM clientes where bajacli is null and dnicli = :dnicli or bajacli is not null and dnicli = :dnicli ORDER BY apelcli, nomecli ASC ")
                query.bindValue(":dnicli", dni)
            else:
                query.prepare("SELECT * FROM clientes where bajacli is null ORDER BY apelcli, nomecli ASC")

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("error listado en conexion ", e)

    def datosOneCliente(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM clientes WHERE dnicli = :dnicli")
            query.bindValue(":dnicli", str(dni))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("error en datos de cliente ", e)

    def modifiCliente(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Select count(*) from clientes where dnicli = :dnicli")
            query.bindValue(":dnicli",str(registro[0]))
            if query.exec():
                if query.next() and query.value(0)>0:
                    if query.exec():
                        query.prepare("UPDATE clientes SET altacli = :altacli, apelcli = :apelcli, nomecli = :nomecli, emailcli = :emailcli,"
                                      " movilcli = :movilcli, dircli = :dircli, provcli = :provcli, municli = :municli, bajacli = :bajacli WHERE dnicli = :dnicli ")
                        query.bindValue(":dnicli", str(registro[0]))
                        query.bindValue(":altacli", str(registro[1]))
                        query.bindValue(":apelcli", str(registro[2]))
                        query.bindValue(":nomecli", str(registro[3]))
                        query.bindValue(":emailcli", str(registro[4]))
                        query.bindValue(":movilcli", str(registro[5]))
                        query.bindValue(":dircli", str(registro[6]))
                        query.bindValue(":provcli", str(registro[7]))
                        query.bindValue(":municli", str(registro[8]))
                        if registro[9] == "":
                            query.bindValue(":bajacli", QtCore.QVariant())
                        else:
                            query.bindValue(":bajacli", str(registro[9]))
                        if query.exec():
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        except Exception as e:
            print("El cliente no está registrado", e)

    @staticmethod
    def bajaCliente(datos):
        query = QtSql.QSqlQuery()
        query.prepare("Select count(*) from clientes where dnicli = :dnicli")
        query.bindValue(":dnicli", str(datos[1]))
        query.exec()
        if query.next() and query.value(0):
            query = QtSql.QSqlQuery()
            query.prepare('UPDATE clientes SET bajacli = :bajacli WHERE dnicli = :dnicli')
            query.bindValue(":bajacli", datetime.now().strftime("%d/%m/%Y"))
            query.bindValue(":dnicli", str(datos[1]))
            if query.exec():
                return True

            else:
                return False


    @staticmethod
    def bajaPropiedad(datos):
        query = QtSql.QSqlQuery()
        query.prepare("Select count(*) from propiedades where codigo = :codigo")
        query.bindValue(":codigo", str(datos[1]))
        query.exec()
        if query.next() and query.value(0):
            query = QtSql.QSqlQuery()
            query.prepare('UPDATE propiedades SET bajaprop = :bajaprop WHERE codigo = :codigo')
            query.bindValue(":bajaprop", str(datos[0]))
            query.bindValue(":codigo", str(datos[1]))
            if query.exec():
                return True

            else:
                return False

    def altaTipoprop(tipo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into tipopropiedad (tipo) values (:tipo) ")
            query.bindValue(":tipo", str(tipo))
            if query.exec():
                registro = Conexion.cargarTipoprop()
                return registro
            else:
                return registro
        except Exception as e:
            print("Error en conexion al dar de alta tipo propiedad", e)

    @staticmethod
    def cargarTipoprop():
        query = QtSql.QSqlQuery()
        query.prepare("SELECT tipo from tipopropiedad ")
        if query.exec():
            registro = []
            while query.next():
                registro.append(str(query.value(0)))
            return registro


    def bajaTipoprop(tipo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE from tipopropiedad where tipo = :tipo ")
            query.bindValue(":tipo", str(tipo))
            if query.exec() and query.numRowsAffected() == 1:
                return True
            else:
                return False
        except Exception as e:
            print("Error en conexion al dar de baja tipo propiedad", e)

    @staticmethod
    def altaPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO PROPIEDADES(altaprop, dirprop, provprop, muniprop, tipoprop, habprop, banprop,"
                          "superprop, prealquilerprop, prevenprop, cpprop, oberprop, tipooper, estadoprop, nomeprop,movilprop)"
                          "VALUES(:altaprop, :dirprop, :provprop, :muniprop, :tipoprop ,:habprop, :banprop, :superprop, :prealquilerprop,"
                          ":prevenprop, :cpprop, :oberprop, :tipooper, :estadoprop, :nomeprop, :movilprop)")
            query.bindValue(":altaprop",str(propiedad[0]))
            query.bindValue(":dirprop",str(propiedad[1]))
            query.bindValue(":provprop",str(propiedad[2]))
            query.bindValue(":muniprop",str(propiedad[3]))
            query.bindValue(":tipoprop",str(propiedad[4]))
            query.bindValue(":habprop",str(propiedad[5]))
            query.bindValue(":banprop",str(propiedad[6]))
            query.bindValue(":superprop",str(propiedad[7]))
            query.bindValue(":prealquilerprop",str(propiedad[8]))
            query.bindValue(":prevenprop",str(propiedad[9]))
            query.bindValue(":cpprop",str(propiedad[10]))
            query.bindValue(":oberprop",str(propiedad[11]))
            query.bindValue(":tipooper",str(propiedad[12]))
            query.bindValue(":estadoprop",str(propiedad[13]))
            query.bindValue(":nomeprop",str(propiedad[14]))
            query.bindValue(":movilprop",str(propiedad[15]))

            if query.exec():
                return True
            else:
                return False


        except Exception as e:
            print("Error al dar de alta propiedad en conexion",e)


    @staticmethod
    def listadoPropiedades():
        try:
            listado = []
            historico = var.ui.chkHistoriaprop.isChecked()
            municipio = var.ui.cmbMuniprop.currentText()
            filtrado = var.ui.btnBuscProp.isChecked()
            tipoSelecionado = var.ui.cmbTipoprop.currentText()

            query = QtSql.QSqlQuery()
            if not historico and filtrado:
                query.prepare("SELECT * FROM propiedades WHERE bajaprop is NULL AND muniprop = :municipio AND tipoprop = :tipo AND estadoprop = 'Disponible'")
                query.bindValue(":municipio", municipio)
                query.bindValue(":tipo", tipoSelecionado)
            elif historico and not filtrado:
                query.prepare("SELECT * FROM propiedades WHERE bajaprop is not NULL or bajaprop is NULL")
            elif historico and filtrado:
                query.prepare("SELECT * FROM propiedades WHERE bajaprop is not NULL or bajaprop is null AND muniprop = :municipio AND tipoprop = :tipo AND estadoprop = 'Disponible'")
                query.bindValue(":municipio", municipio)
                query.bindValue(":tipo", tipoSelecionado)

            else:
                query.prepare("SELECT * FROM propiedades WHERE bajaprop is NULL AND estadoprop = 'Disponible'")

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado

        except Exception as e:
            print("Error en listado de propiedades en conexion", e)


    def modifProp(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from propiedades where codigo = :codigo")
            query.bindValue(":codigo", propiedad[0])
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1: #verificamos que solo nos devuelve un resultado, la fila para el codigo que buscamos
                    query.prepare("UPDATE propiedades set altaprop = :altaprop, bajaprop = :bajaprop, dirprop = :dirprop, "
                                  "muniprop = :muniprop, provprop = :provprop, "
                                  "tipoprop = :tipoprop, habprop=:habprop, banprop = :banprop, "
                                  "superprop = :superprop, prealquilerprop = :prealquilerprop, prevenprop = :prevenprop, "
                                  "cpprop = :cpprop, oberprop = :oberprop, tipooper = :tipooper,"
                                  " estadoprop=:estadoprop, nomeprop =:nomeprop, movilprop =:movilprop WHERE codigo = :codigo")
                    query.bindValue(":codigo",str(propiedad[0]))
                    query.bindValue(":altaprop",str(propiedad[1]))
                    query.bindValue(":dirprop",str(propiedad[3]))
                    query.bindValue(":provprop",str(propiedad[4]))
                    query.bindValue(":muniprop",str(propiedad[5]))
                    query.bindValue(":tipoprop",str(propiedad[6]))
                    query.bindValue(":habprop",str(propiedad[7]))
                    query.bindValue(":banprop",str(propiedad[8]))
                    query.bindValue(":superprop",str(propiedad[9]))
                    query.bindValue(":prealquilerprop",str(propiedad[10]))
                    query.bindValue(":prevenprop",str(propiedad[11]))
                    query.bindValue(":cpprop",str(propiedad[12]))
                    query.bindValue(":oberprop",str(propiedad[13]))
                    query.bindValue(":tipooper",str(propiedad[14]))
                    query.bindValue(":estadoprop",str(propiedad[15]))
                    query.bindValue(":nomeprop",str(propiedad[16]))
                    query.bindValue(":movilprop",str(propiedad[17]))
                    if propiedad[2] == "":
                        query.bindValue(":bajacli",QtCore.QVariant()) #QVariant añade un null a la BD
                    else:
                        query.bindValue(":bajaprop",str(propiedad[2]))
                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        except Exception as e:
            print("Error al modificar cliente en conexión.",e)

    @staticmethod
    def datosOnePropiedad(codigo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error al cargar UNA propiedad en conexion.", e)

    @staticmethod
    def datosOnePropiedadBusq(municipio, provincia):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE muniprop = :muniprop AND provprop = :provprop AND estadoprop = 'Disponible'")
            query.bindValue(":muniprop", str(municipio))
            query.bindValue(":provprop", str(provincia))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error al cargar UNA propiedad en conexion.", e)

    @staticmethod
    def listadoPropiedadesExportar():
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE bajaprop is NULL or bajaprop is not null")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error al exportar", e)


    @staticmethod
    def ListadoClientesExportar():
        listado = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC")
        if query.exec():
            while query.next():
                fila = [query.value(i) for i in range(query.record().count())]
                listado.append(fila)
        return listado


    '''
        Zona vendedores
    '''

    def altaVendedor(nuevoVendedor):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO VENDEDOR(dniVendedor, nombreVendedor, altaVendedor, bajaVendedor, "
                          "movilVendedor, mailVendedor, delegacionVendedor) VALUES (:dniVendedor, :nombreVendedor,:altaVendedor,"
                          ":bajaVendedor,:movilVendedor,:mailVendedor,:delegacionVendedor)")
            query.bindValue(":dniVendedor", str(nuevoVendedor[0]))
            query.bindValue(":nombreVendedor", str(nuevoVendedor[1]))
            query.bindValue(":altaVendedor", str(nuevoVendedor[2]))
            query.bindValue(":bajaVendedor", str(nuevoVendedor[3]))
            query.bindValue(":movilVendedor", str(nuevoVendedor[4]))
            query.bindValue(":mailVendedor", str(nuevoVendedor[5]))
            query.bindValue(":delegacionVendedor", str(nuevoVendedor[6]))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error en alta cliente ", e)

    @staticmethod
    def listadoVendedores():
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idVendedor, nombreVendedor, movilVendedor, delegacionVendedor FROM vendedor ORDER BY idVendedor ASC ")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("error listado en conexion ", e)


    def modifiVendedores(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Select count(*) from vendedor where idVendedor = :idVendedor")
            query.bindValue(":idVendedor",str(registro[0]))
            if query.exec():
                if query.next() and query.value(0)>0:
                    if query.exec():
                        query.prepare("UPDATE vendedor SET nombreVendedor = :nombreVendedor,  altaVendedor = :altaVendedor, bajaVendedor = :bajaVendedor,"
                                      "movilVendedor = :movilVendedor, mailVendedor =:mailVendedor, delegacionVendedor = :delegacionVendedor WHERE idVendedor = :idVendedor ")
                        query.bindValue(":idVendedor", str(registro[0]))
                        query.bindValue(":nombreVendedor", str(registro[1]))
                        query.bindValue(":altaVendedor", str(registro[2]))
                        query.bindValue(":movilVendedor", str(registro[4]))
                        query.bindValue(":mailVendedor", str(registro[5]))
                        query.bindValue(":delegacionVendedor", str(registro[6]))
                        if registro[2] == "":
                            query.bindValue(":bajaVendedor", QtCore.QVariant())
                        else:
                            query.bindValue(":bajaVendedor", str(registro[3]))
                        if query.exec():
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        except Exception as e:
            print("El cliente no está registrado", e)

    @staticmethod
    def bajaVendedor(datos):
        query = QtSql.QSqlQuery()
        query.prepare("Select count(*) from vendedor where idVendedor = :idVendedor")
        query.bindValue(":idVendedor", str(datos[1]))
        query.exec()
        if query.next() and query.value(0):
            query = QtSql.QSqlQuery()
            query.prepare('UPDATE vendedor SET bajaVendedor = :bajaVendedor WHERE idVendedor = :idVendedor')
            query.bindValue(":bajaVendedor", datetime.now().strftime("%d/%m/%Y"))
            query.bindValue(":idVendedor", str(datos[1]))
            if query.exec():
                return True
            else:
                return False

    def datosOneVendedor(codigo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idVendedor,dniVendedor,nombreVendedor,altaVendedor,bajaVendedor, movilVendedor,mailVendedor, delegacionVendedor FROM vendedor WHERE idVendedor = :idVendedor")
            query.bindValue(":idVendedor", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("error en datos de cliente ", e)