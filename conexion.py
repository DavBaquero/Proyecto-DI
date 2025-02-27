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
        """

        :param self: None
        :type self: None
        :return: False or True
        :rtype: Boolean

        Módulo de conexión a la base de datos
        Si éxito, devuelve True, si no, False

        """
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
        """

        :param self: None
        :type self: None
        :return: lista de provincias
        :rtype: bytearray

        Metodo que devuelve una lista de provincias de la base de datos

        """
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def listaMuni(provincia):
        """

        :param provincia:
        :type provincia: string
        :return: retorna una lista de municipios
        :rtype: bytearray

        Metodo que devuelve una lista de municipios segun la provincia de la base de datos

        """
        listamunicipios = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = ?)")
        query.bindValue(0, provincia)

        if query.exec():
            while query.next():
                listamunicipios.append(query.value(1))
        return listamunicipios

    def altaCliente(nuevocli):
        """
        :param nuevocli: Lista con los datos del cliente
        :type nuevocli: list
        :return: retorna True si se ha dado de alta correctamente, False si no
        :rtype: boolean

        Metodo que da de alta un cliente en la base de datos

        """
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
        """
        :param self: None
        :type self: None
        :return: retorna una lista de clientes
        :rtype: list

        Metodo que devuelve una lista de clientes de la base de datos ordenados por apellidos y nombre

        """
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
        """
        :param dni: String con el dni del cliente
        :type dni: string
        :return: retorna una lista con los datos del cliente
        :rtype: list

        Metodo que devuelve una lista con los datos de un cliente de la base de datosç

        """
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
        """
        :param registro: Lista con los datos del cliente
        :type registro: list
        :return: retorna True si se ha modificado correctamente, False si no
        :rtype: boolean

        Metodo que modifica un cliente en la base de datos

        """
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
        """

        :param datos: lista con algunos datos del cliente
        :type datos: list
        :return: retorna True si se ha dado de baja correctamente, False si no
        :rtype: boolean

        Metodo que da de baja un cliente en la base de datos
        """
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
        """

        :param datos: Lista con algunos datos de la propiedad
        :type datos: list
        :return: retorna True si se ha dado de baja correctamente, False si no
        :rtype: boolean

        Metodo que da de baja una propiedad en la base de datos

        """
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
        """
        :param tipo: Lista con los datos del tipo de propiedad
        :type tipo: list
        :return: retorna una lista con los tipos de propiedad nuevos
        :rtype: list

        Metodo que da de alta un tipo de propiedad en la base de datos
        """
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
        """
        :param self: None
        :type self: None
        :return: retorna una lista con los tipos de propiedad
        :rtype: list

        Metodo que devuelve una lista con los tipos de propiedad de la base de datos

        """
        query = QtSql.QSqlQuery()
        query.prepare("SELECT tipo from tipopropiedad ")
        if query.exec():
            registro = []
            while query.next():
                registro.append(str(query.value(0)))
            return registro


    def bajaTipoprop(tipo):
        """
        :param tipo: String con el tipo de propiedad
        :type tipo: string
        :return: retorna True si se ha dado de baja correctamente, False si no
        :rtype: boolean

        Metodo que da de baja un tipo de propiedad en la base de datos

        """
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
        """

        :param propiedad: Lista con los datos de la propiedad
        :type propiedad: list
        :return: retorna True si se ha dado de alta correctamente, False si no
        :rtype: boolean

        Metodo que da de alta una propiedad en la base de datos

        """
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
        """
        :param self: None
        :type self: None
        :return: retorna una lista con las propiedades
        :rtype: list

        Metodo que devuelve una lista con las propiedades de la base de datos

        """
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
        """
        :param propiedad: Lista con los datos de la propiedad
        :type propiedad: list
        :return: retorna True si se ha modificado correctamente, False si no
        :rtype: boolean

        Metodo que modifica una propiedad en la base de datos

        """
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
    def cargarMunicipios():
        try:
            listaMuni = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM MUNICIPIOS")
            if query.exec():
                while query.next():
                    listaMuni.append(query.value(1))
                return listaMuni
        except Exception as e:
            print('Error cargando municipios')

    @staticmethod
    def datosOnePropiedad(codigo):
        """

        :param codigo: String con el codigo de la propiedad
        :type codigo: string
        :return: retorna una lista con los datos de la propiedad
        :rtype: list

        Metodo que devuelve una lista con los datos de una propiedad de la base de datos

        """
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
        """

        :param municipio: String con el municipio de la propiedad
        :type municipio: string
        :param provincia: String con la provincia de la propiedad
        :type provincia: string
        :return: retorna una lista con los datos de la propiedad
        :rtype: list

        Metodo que devuelve una lista con los datos de una propiedad de la base de datos
        """
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
        """
        :param self: None
        :type self: None
        :return: retorna una lista con las propiedades
        :rtype: list

        Metodo que devuelve una lista con las propiedades de la base de datos para exportar
        """
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
        """
        :param self: None
        :type self: None
        :return: retorna una lista con los clientes
        :rtype: list

        Metodo que devuelve una lista con los clientes de la base de datos para exportar

        """
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
        """
        :param nuevoVendedor: Lista con los datos del vendedor
        :type nuevoVendedor: list
        :return: retorna True si se ha dado de alta correctamente, False si no
        :rtype: boolean

        Metodo que da de alta un vendedor en la base de datos

        """
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
        """
        :param self: None
        :type self: None
        :return: retorna una lista con los vendedores
        :rtype: list

        Metodo que devuelve una lista con los vendedores de la base de datos

        """
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
        """
        :param registro: Lista con los datos del vendedor
        :type registro: list
        :return: retorna True si se ha modificado correctamente, False si no
        :rtype: boolean

        Metodo que modifica un vendedor en la base de datos
        """
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
        """

        :param datos: lista con algunos datos del vendedor
        :type datos: list
        :return: retorna True si se ha dado de baja correctamente, False si no
        :rtype: boolean

        Metodo que da de baja un vendedor en la base de datos
        """
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
        """
        :param codigo: String con el codigo del vendedor
        :type codigo: string
        :return: retorna una lista con los datos del vendedor
        :rtype: list

        Metodo que devuelve una lista con los datos de un vendedor de la base de datos
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idVendedor,dniVendedor,nombreVendedor,altaVendedor,bajaVendedor,"
                          " movilVendedor,mailVendedor, delegacionVendedor FROM vendedor WHERE idVendedor = :idVendedor")
            query.bindValue(":idVendedor", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("error en datos de cliente ", e)


    '''
        Zona de facturas
    '''

    @staticmethod
    def altaFactura(registro):
        """

        :param registro: Una lista que contiene la fecha de la factura y el dni del cliente
        :type registro: List
        :return: True or false
        :rtype: Boolean

        Metodo encargado de dar de alta una factura en la BD

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO FACTURAS (fechafac, dnifac) VALUES (:fechafac, :dnifac)")
            query.bindValue(":fechafac", registro[0])
            query.bindValue(":dnifac", registro[1])
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al dar de alta factura en conexion:", e)
            return False

    @staticmethod
    def listadoFacturas():
        """

        :return: Lista de facturas
        :rtype: List

        Metodo encargado de devolver una lista con todas las facturas

        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT id, dnifac, fechafac FROM facturas")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listando facturas en listadoFacturas - conexión", e)

    @staticmethod
    def bajaFactura(idFactura):
        """

        :param idFactura: La id de la factura
        :type idFactura: String
        :return: True or false
        :rtype: Boolean

        Metodo encargado de dar de baja una factura

        """
        try:
            query1 = QtSql.QSqlQuery()
            query1.prepare("Select count(*) from ventas where facventa = :facventa")
            query1.bindValue(":facventa", str(idFactura))
            if query1.exec() and query1.next() and query1.value(0) == 0:
                query = QtSql.QSqlQuery()
                query.prepare("DELETE FROM facturas WHERE id = :id")
                query.bindValue(":id", str(idFactura))
                if query.exec():
                    return True
                else:
                    error = query.lastError()
                    if error is not None:
                        print("Error en la ejecución de la consulta:", error.text())
                    return False
            else:
                mbox = eventos.Eventos.crearMensajeError("Error baja factura","No se puede eliminar la factura porque tiene ventas asociadas")
                mbox.exec()
        except Exception as e:
            print("Error eliminando factura en bajaFactura - conexión:", e)
            return False

    @staticmethod
    def cargaOneFactura(idFactura):
        """

        :param idFactura: La id de la factura
        :type idFactura: String
        :return: Lista con los datos de una factura
        :rtype: List

        Metodo para buscar una factura en concreto
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas WHERE id = :id")
            query.bindValue(":id", idFactura)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error cargando factura en cargaOneFactura - conexión", e)


    '''
        Zona de ventas
    '''

    @staticmethod
    def altaVenta(registro):
        """

        :param registro: Lista con los datos de la venta
        :type registro: List
        :return: True or false
        :rtype: Boolean

        Metodo para dar de alta una venta

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO ventas (facventa, codprop, agente) VALUES (:facventa, :codprop, :agente)")
            query.bindValue(":facventa", str(registro[0]))
            query.bindValue(":codprop", str(registro[1]))
            query.bindValue(":agente", str(registro[2]))
            if query.exec():
                return True
            else:
                print("Error en la ejecución de la consulta:", query.lastError().text())
                return False
        except Exception as e:
            print("Error al dar de alta factura en conexion:", e)
            return False

    @staticmethod
    def listadoVentas(idFactura):
        """

        :param idFactura: La id de la factura a la que está asociada la venta
        :type idFactura: String
        :return: Listado con todas las ventas y sus datos asociados a la factura
        :rtype: List

        Metodo encargado de buscar las ventas en la BD

        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT v.idventa, v.codprop, p.dirprop, p.muniprop, p.tipoprop, "
                "p.prevenprop FROM ventas AS v INNER JOIN propiedades as p on v.codprop = p.codigo WHERE v.facventa = :facventa")
            query.bindValue(":facventa", str(idFactura))
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listando facturas en listadoFacturas - conexión", e)

    @staticmethod
    def datosOneVenta(idVenta):
        """

        :param idVenta: La id de la venta
        :type idVenta: String
        :return: Lista con los datos de una venta
        :rtype: List

        Metodo para buscar una venta

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT v.agente, v.codprop, p.tipoprop, p.prevenprop,"
                " p.muniprop, p.dirprop  FROM ventas as v "
                "INNER JOIN propiedades as p ON v.codprop = p.codigo WHERE v.idventa = :idventa")
            query.bindValue(":idventa", str(idVenta))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            else:
                print("Error en la ejecución de la consulta:", query.lastError().text())
            return registro
        except Exception as e:
            print("Error en datosOneVenta en conexion", e)

    @staticmethod
    def actualizaPropiedadVenta(codigoPropiedad):
        """

        :param codigoPropiedad: Es la id de la propiedad
        :type codigoPropiedad: String
        :return: True o false
        :rtype: Boolean

        Metodo para dar de baja una propiedad justo después de que se asocie a una venta

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET estadoprop = 'Vendido', bajaprop = :fechaBaja WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigoPropiedad))
            query.bindValue(":fechaBaja", datetime.now().strftime("%d/%m/%Y"))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al vender una Propiedad en conexion.", e)


    def bajaVenta(idVenta):
        """

        :param idVenta: La id de la venta
        :type idVenta: String
        :return: True or false
        :rtype: Boolean

        Metodo para borrar una venta de la bd
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM ventas WHERE idventa = :idventa")
            query.bindValue(":idventa", str(idVenta))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al eliminar una venta en conexion.", e)
            return False

    @staticmethod
    def altaPropiedadVenta(codigoPropiedad):
        """

               :param codigoPropiedad: Es la id de la propiedad
               :type codigoPropiedad: String
               :return: True o false
               :rtype: Boolean

               Metodo para dar de alta una propiedad justo después de que se deje de asociar a una venta

               """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "UPDATE propiedades SET estadoprop = 'Disponible', bajaprop = :fechaBaja WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigoPropiedad))
            query.bindValue(":fechaBaja", QtCore.QVariant())
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al vender una Propiedad en conexion.", e)


    '''
        Zona de Alquileres
    '''

    @staticmethod
    def altaAlquiler(Alquiler):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO ALQUILERES (propiedad_id,cliente_dni,fecha_inicio,fecha_fin,vendedor) "
                          "VALUES (:propiedad_id,:cliente_dni,:fecha_inicio,:fecha_fin,:vendedor)")
            query.bindValue(":propiedad_id", str(Alquiler[0]))
            query.bindValue(":cliente_dni", str(Alquiler[1]))
            query.bindValue(":fecha_inicio", str(Alquiler[2]))
            query.bindValue(":fecha_fin", str(Alquiler[3]))
            query.bindValue(":vendedor", str(Alquiler[4]))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al dar de alta alquiler en conexion:", e)
            return False

    @staticmethod
    def actualizaPropiedadAlquiler(codigoPropiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET estadoprop = 'Alquilado', bajaprop = :fechaBaja WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigoPropiedad))
            query.bindValue(":fechaBaja", datetime.now().strftime("%d/%m/%Y"))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al alquilar una Propiedad en conexion.", e)
            return False

    @staticmethod
    def checkPropiedadAlq(idPropiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM alquileres WHERE propiedad_id = :idPropiedad")
            query.bindValue(":idPropiedad", str(idPropiedad))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False
        except Exception as e:
            print("Error al comprobar si una propiedad está alquilada en conexion.", e)
            return False

    @staticmethod
    def checkPorpiedadVen(idPropiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM ventas WHERE codprop = :idPropiedad")
            query.bindValue(":idPropiedad", str(idPropiedad))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False
        except Exception as e:
            print("Error al comprobar si una propiedad está vendida en conexion.", e)
            return False

    @staticmethod
    def listadoContrato():
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT a.id, a.cliente_dni FROM alquileres AS a")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listando contratos en listadoContrato - conexión", e)

    @staticmethod
    def cargaOneContrato(idAlquiler):
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("Select id, fecha_inicio, fecha_fin from alquileres")
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        listado.append(str(query.value(i)))
            return listado
        except Exception as e:
            print("Error en la query de cargar un contrato: ",e)

    @staticmethod
    def buscarAlquiler(p,c):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select id from alquileres where propiedad_id = :p and cliente_dni = :c")
            query.bindValue(":p",p)
            query.bindValue(":c",c)
            if query.exec():
                while query.next():
                    return query.value(0)
        except Exception as e:
            print("Error en la query de buscar un alquiler: ", e)

    @staticmethod
    def altaMensualidad(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO mensualidades(idalquiler, mes, pagado) VALUES (:idalquiler,:mes,:pagado)")
            query.bindValue(":idalquiler", str(registro[0]))
            query.bindValue(":mes", str(registro[1]))
            query.bindValue(":pagado", str(registro[2]))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al grabar nueva mensualidad en conexion", str(e))