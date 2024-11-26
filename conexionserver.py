import datetime

import mysql.connector
from mysql.connector import Error
import os
from PyQt6 import QtSql, QtWidgets, QtCore

import var


class ConexionServer():
    def crear_conexion(self):

        try:
            conexion = mysql.connector.connect(
            host='192.168.10.66', # Cambia esto a la IP de tu servidor user='dam', # Usuario creado
            #host='192.168.1.49',
            user='dam',
            password='dam2425',
            database='bbdd',
            charset="utf8mb4",
            collation="utf8mb4_general_ci"  # Asegúrate de que aquí esté configurado
            # Contraseña del usuario database='bbdd' # Nombre de la base de datos
            )
            if conexion.is_connected():
                pass
                #print("Conexión exitosa a la base de datos")
            return conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        return None

    @staticmethod
    def listaProv(self=None):
        listaprov = []
        conexion = ConexionServer().crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM provincias")
                resultados = cursor.fetchall()
                for fila in resultados:
                    listaprov.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
                cursor.close()
                conexion.close()
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
        return listaprov

    @staticmethod
    def listaMuniProv(provincia):
        try:
            conexion = ConexionServer().crear_conexion()
            listamunicipios = []
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = %s)",
                (provincia,)
            )
            resultados = cursor.fetchall()
            for fila in resultados:
                listamunicipios.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
            cursor.close()
            conexion.close()
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

    def listadoClientes(self):
        try:
            conexion = ConexionServer().crear_conexion()
            listadoclientes = []
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC")
            resultados = cursor.fetchall()
            for fila in resultados:      # Procesar cada fila de los resultados y crea una lista con valores de la fila
                listadoclientes.append(list(fila))  # Convierte la tupla en una lista y la añade a listadoclientes
            cursor.close()    # Cerrar el cursor y la conexión si no los necesitas más
            conexion.close()
            return listadoclientes
        except Exception as e:
            print("error listado en conexion", e)

    def altaCliente(cliente):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                INSERT INTO clientes (dnicli, altacli, apelcli, nomecli, dircli, emailcli, movilcli, provcli, municli)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, cliente)          # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()   # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")

    def datosOneCliente(dni):
        registro = []  # Inicializa la lista para almacenar los datos del cliente
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de selección
                query = '''SELECT dnicli, altacli, apelcli, nomecli, dircli, emailcli, movilcli, provcli, municli, bajacli FROM clientes WHERE dnicli = %s'''  # Usa %s para el placeholder
                cursor.execute(query, (dni,))  # Pasar 'dni' como una tupla
                # Recuperar los datos de la consulta
                for row in cursor.fetchall():
                    registro.extend([str(col) for col in row])
            return registro

        except Exception as e:
            print("Error al obtener datos de un cliente:", e)
            return None  # Devolver None en caso de error

    def modifiCliente(registro):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                query = """UPDATE clientes SET altacli = %s, apelcli = %s, 
                nomecli = %s, dircli = %s, emailcli = %s, movilcli = %s, provcli = %s,
                municli = %s, bajacli = %s WHERE dnicli = %s"""
                cursor.execute(query, registro)
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Exception as e:
            print("El cliente no está registrado", e)
            return False



    @staticmethod
    def bajaCliente(fecha, dni):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                datos = (fecha, dni)
                cursor = conexion.cursor()
                query = """UPDATE clientes SET bajacli = %s WHERE dnicli = %s"""
                cursor.execute(query, datos)
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Exception as e:
            print("El cliente no está registrado", e)



    @staticmethod
    def listadoPropiedades():
        try:
            historico = var.ui.chkHistoriaprop.isChecked()
            municipio = var.ui.cmbMuniprop.currentText()
            filtrado = var.ui.btnBuscProp.isChecked()
            tipoSelecionado = var.ui.cmbTipoprop.currentText()

            conexion = ConexionServer().crear_conexion()
            listadopropiedades = []
            cursor = conexion.cursor()
            if not historico and filtrado:
                cursor.execute("SELECT * FROM propiedades WHERE bajaprop is NULL AND muniprop = '"+municipio+"' AND tipoprop = '"+tipoSelecionado+"' AND estadoprop = 'Disponible'")
                resultados = cursor.fetchall()
            elif historico and not filtrado:
                cursor.execute("SELECT * FROM propiedades WHERE bajaprop is not NULL or bajaprop is NULL")
                resultados = cursor.fetchall()
            elif historico and filtrado:
                cursor.execute("SELECT * FROM propiedades WHERE bajaprop is not NULL or bajaprop is null AND muniprop = '"+municipio+"' AND tipoprop = '"+tipoSelecionado+"' AND estadoprop = 'Disponible'")
                resultados = cursor.fetchall()
            else:
                cursor.execute("SELECT * FROM propiedades WHERE bajaprop is NULL AND estadoprop = 'Disponible'")
                resultados = cursor.fetchall()

            for fila in resultados:
                listadopropiedades.append(list(fila))
            cursor.close()
            conexion.close()
            return listadopropiedades

        except Exception as e:
            print("Error en listado de propiedades en conexion", e)


    @staticmethod
    def datosOnePropiedad(codigo):
        registro = []  # Inicializa la lista para almacenar los datos del cliente
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                query = """SELECT * FROM propiedades WHERE CODIGO = %s"""
                cursor.execute(query, (codigo,))  # Pasar 'dni' como una tupla
            # Recuperar los datos de la consulta
                for row in cursor.fetchall():
                    registro.extend([str(col) for col in row])
                return registro
        except Exception as e:
            print("Error al cargar UNA propiedad en conexion.", e)

    @staticmethod
    def listaProvprop(self=None):
        listaprov = []
        conexion = ConexionServer().crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM provincias")
                resultados = cursor.fetchall()
                for fila in resultados:
                    listaprov.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
                cursor.close()
                conexion.close()
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
        return listaprov

    @staticmethod
    def listaMuniProvprop(provincia):
        try:
            conexion = ConexionServer().crear_conexion()
            listamunicipios = []
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = %s)",
                (provincia,)
            )
            resultados = cursor.fetchall()
            for fila in resultados:
                listamunicipios.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
            cursor.close()
            conexion.close()
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)


    @staticmethod
    def cargarTipoprop():
        conexion = ConexionServer().crear_conexion()
        listaTipoProp = []
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT tipo from tipopropiedad ")
                resultados = cursor.fetchall()
                for fila in resultados:
                    listaTipoProp.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
                cursor.close()
                conexion.close()
            except Exception as e:
                print("Error cargar tipo", e)

    def altaTipoprop(tipo):
        try:
            registro = []
            conexion = ConexionServer().crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("INSERT into tipopropiedad (tipo) values (%s) ")
            cursor.fetchall()

            if cursor.execute():
                registro = ConexionServer.cargarTipoprop()
                return registro
            else:
                return registro
        except Exception as e:
            print("Error en conexion al dar de alta tipo propiedad", e)