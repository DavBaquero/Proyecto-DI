from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.graphics import renderPM
import os

import conexion
import eventos
import var
from PIL import Image
from svglib.svglib import svg2rlg
from PyQt6 import QtWidgets,QtSql, QtCore
import sqlite3

class Informes:

    @staticmethod
    def reportClientes(self):
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today()
            fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
            nompdfcli = fecha + "_listadoclientes.pdf"
            pdf_path = os.path.join(rootPath, nompdfcli)

            # Primer pase para contar páginas
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado clientes"
            items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
            query = QtSql.QSqlQuery()
            query.prepare('select dnicli, apelcli, nomecli, movilcli, provcli, municli from clientes order by apelcli')
            total_pages = 1
            if query.exec():
                y = 635
                while query.next():
                    if y <= 95:
                        total_pages += 1
                        y = 635
                    y -= 20

            # Segundo pase para generar el informe
            var.report = canvas.Canvas(pdf_path)
            Informes.topInforme(titulo)
            Informes.footInforme(titulo, total_pages)
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 650, str(items[0]))
            var.report.drawString(100, 650, str(items[1]))
            var.report.drawString(190, 650, str(items[2]))
            var.report.drawString(285, 650, str(items[3]))
            var.report.drawString(360, 650, str(items[4]))
            var.report.drawString(450, 650, str(items[5]))
            var.report.line(50, 645, 525, 645)
            if query.exec():
                x = 55
                y = 635
                while query.next():
                    if y <= 95:
                        var.report.setFont('Helvetica-Oblique', size=9)
                        var.report.drawString(450, 90, "Página siguiente...")
                        var.report.showPage()
                        Informes.footInforme(titulo, total_pages)
                        Informes.topInforme(titulo)
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 650, str(items[0]))
                        var.report.drawString(100, 650, str(items[1]))
                        var.report.drawString(190, 650, str(items[2]))
                        var.report.drawString(285, 650, str(items[3]))
                        var.report.drawString(360, 650, str(items[4]))
                        var.report.drawString(450, 650, str(items[5]))
                        var.report.line(50, 645, 525, 645)
                        x = 55
                        y = 635
                    var.report.setFont("Helvetica", size=9)
                    dni = "***" + str(query.value(0)[4:7] + "***")
                    var.report.drawCentredString(x + 10, y, str(dni))
                    var.report.drawString(x + 45, y, str(query.value(1).title()))
                    var.report.drawString(x + 135, y, str(query.value(2).title()))
                    var.report.drawString(x + 230, y, str(query.value(3).title()))
                    var.report.drawString(x + 305, y, str(query.value(4).title()))
                    var.report.drawString(x + 395, y, str(query.value(5).title()))
                    y -= 20

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nompdfcli):
                    os.startfile(pdf_path)

        except Exception as e:
            print(e)

    def footInforme(titulo, total_pages):
        try:
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, f'Página {var.report.getPageNumber()} de {total_pages}')
        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)


    def topInforme(titulo):
        try:
            ruta_logo_svg = '.\\img\\logo.svg'
            ruta_logo_png = '.\\img\\logo.png'

            # Convertir SVG a PNG
            logo = svg2rlg(ruta_logo_svg)
            renderPM.drawToFile(logo, ruta_logo_png, fmt='PNG')

            # Cargar la imagen PNG
            logo = Image.open(ruta_logo_png)

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image):
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'Inmobiliaria Teis')
                var.report.drawString(230, 680, titulo)
                var.report.line(50, 665, 525, 665)

                # Dibuja la imagen en el informe
                var.report.drawImage(ruta_logo_png, 480, 725, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawString(55, 770, 'CIF: A12345678')
                var.report.drawString(55, 755, 'Avda. Galicia - 101')
                var.report.drawString(55, 740, 'Vigo - 36216 - España')
                var.report.drawString(55, 725, 'Teléfono: 986 132 456')
                var.report.drawString(55, 710, 'e-mail: cartesteisr@mail.com')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo_png}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    @staticmethod
    def reportPropiedades(municipio):
        try:
            ymax = 635
            ymin = 90
            ystep = 20
            xmin = 60
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            titulo = "Listado Propiedades"
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdfcli = fecha + "_listadopropiedades.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)

            # Primer pase para contar páginas
            var.report = canvas.Canvas(pdf_path)
            items = ['COD', 'DIRECCION', 'TIPO PROP.', 'OPERACION', 'PRECIO ALQ.', 'PRECIO VENTA']
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT codigo, dirprop, tipoprop, tipooper, prealquilerprop, prevenprop FROM propiedades WHERE muniprop = :municipio ORDER BY muniprop")
            query.bindValue(":municipio", str(municipio))
            total_pages = 1
            if query.exec():
                y = ymax
                while query.next():
                    if y <= ymin:
                        total_pages += 1
                        y = ymax
                    y -= ystep
            else:
                print("Error en la consulta SQL:", query.lastError().text())
            # Segundo pase para generar el informe
            var.report = canvas.Canvas(pdf_path)
            Informes.topInforme(titulo)
            Informes.footInforme(titulo, total_pages)
            var.report.drawString(55, 650, str(items[0]))
            var.report.drawString(100, 650, str(items[1]))
            var.report.drawString(210, 650, str(items[2]))
            var.report.drawString(295, 650, str(items[3]))
            var.report.drawString(380, 650, str(items[4]))
            var.report.drawString(460, 650, str(items[5]))
            if query.exec():
                x = xmin
                y = ymax
                while query.next():
                    if y <= ymin:
                        var.report.setFont('Helvetica-Oblique', size=10)
                        var.report.drawString(450, 80, "Página siguiente...")
                        var.report.showPage()
                        Informes.footInforme(titulo, total_pages)
                        Informes.topInforme(titulo)
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 650, str(items[0]))
                        var.report.drawString(100, 650, str(items[1]))
                        var.report.drawString(210, 650, str(items[2]))
                        var.report.drawString(295, 650, str(items[3]))
                        var.report.drawString(380, 650, str(items[4]))
                        var.report.drawString(460, 650, str(items[5]))
                        var.report.line(40, 625, 540, 625)
                        x = xmin
                        y = ymax
                    var.report.setFont('Helvetica-Oblique', size=10)
                    var.report.drawString(x + 5, y, str(query.value(0)))
                    var.report.drawString(x + 40, y, str(query.value(1)))
                    var.report.drawString(x + 150, y, str(query.value(2)))
                    operacion = query.value(3).replace("[", "").replace("]", "").replace("'", "")
                    var.report.drawString(x + 240, y, str(operacion))
                    alquiler = "-" if not str(query.value(4)) else str(query.value(4))
                    var.report.drawRightString(x + 380, y, alquiler + " €")
                    compra = "-" if not str(query.value(5)) else str(query.value(5))
                    var.report.drawRightString(x + 470, y, compra + " €")
                    y -= ystep
            else:
                print("Error en la consulta SQL:", query.lastError().text())
                print(query.lastError().text())
            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as e:
            print(e)

    @staticmethod
    def reportFact(idFactura):
        xidventa = 55
        xidpropiedad = xidventa + 35
        xdireccion = xidpropiedad + 50
        xlocalidad = xdireccion + 150
        xtipo = xlocalidad + 100
        xprecio = xtipo + 50
        try:
            if ((idFactura != None) and (idFactura != "")):
                rootPath = '.\\informes'
                if not os.path.exists(rootPath):
                    os.makedirs(rootPath)
                fecha = datetime.today()
                fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
                nompdfcli = fecha + "_FacturaVentas.pdf"
                pdf_path = os.path.join(rootPath, nompdfcli)

                var.report = canvas.Canvas(pdf_path)
                titulo = "Factura Código " + idFactura
                listado_ventas = conexion.Conexion.listadoVentas(idFactura)
                factura = conexion.Conexion.cargaOneFactura(idFactura)
                cliente = conexion.Conexion.datosOneCliente(factura[2])
                Informes.topInforme(titulo)
                Informes.topDatosCliente(cliente, factura[1])
                Informes.footInforme(titulo, 1)
                items = ["ID VENTA", "CÓDIGO", "DIRECCIÓN", "LOCALIDAD", "TIPO", "PRECIO"]
                Informes.footInforme(titulo, "1")
                var.report.setFont("Helvetica-Bold", size=10)
                var.report.drawString(55, 650, str(items[0]))
                var.report.drawString(110, 650, str(items[1]))
                var.report.drawString(160, 650, str(items[2]))
                var.report.drawString(290, 650, str(items[3]))
                var.report.drawString(390, 650, str(items[4]))
                var.report.drawString(440, 650, str(items[5]))
                var.report.line(50, 645, 525, 645)
                y = 630
                for registro in listado_ventas:
                    var.report.setFont("Helvetica", size=8)
                    var.report.drawCentredString(75, y, str(registro[0]))
                    var.report.drawCentredString(120, y, str(registro[1]).title())
                    var.report.drawString(170, y, str(registro[2]).title())
                    var.report.drawString(300, y, str(registro[3]).title())
                    var.report.drawString(390, y, str(registro[4]).title())
                    var.report.drawCentredString(470, y, str(registro[5]).title() + " €")
                    y -= 30

                var.report.save()

                for file in os.listdir(rootPath):
                    if file.endswith(nompdfcli):
                        os.startfile(pdf_path)
            else:
                mbox = eventos.Eventos.crearMensajeError("Error ifrome factura", "No se ha seleccionado ninguna factura")
                mbox.exec()
        except Exception as e:
            print("Error reportFact = ",e )


    @staticmethod
    def topDatosCliente(cliente, fecha):
        try:
            var.report.setFont('Helvetica-Bold', size=8)
            var.report.drawString(300, 770, 'DNI Cliente:')
            var.report.drawString(300, 752, 'Nombre:')
            var.report.drawString(300, 734, 'Dirección:')
            var.report.drawString(300, 716, 'Localidad:')
            var.report.drawString(55, 682, "Fecha Factura:")
            var.report.setFont('Helvetica', size=8)
            var.report.drawString(360, 770, cliente[0])
            var.report.drawString(360, 752, cliente[3] + " " + cliente[2])
            var.report.drawString(360, 734, cliente[6])
            var.report.drawString(360, 716, cliente[8])
            var.report.drawString(120, 682, fecha)
        except Exception as error:
            print('Error en cabecera informe:', error)

    @staticmethod
    def reportReciboMensualidad(idAlquiler, idMensualidad):
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            titulo = "RECIBO MENSUALIDAD ALQUILER"
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdffac = fecha + "_recibo_alquiler_" + str(idAlquiler) + ".pdf"
            pdf_path = os.path.join(rootPath, nomepdffac)
            var.report = canvas.Canvas(pdf_path)

            datosAlq = conexion.Conexion.datosOneAlquiler(idAlquiler)
            fechaini = datosAlq[1]
            fechafin = datosAlq[2]
            idVendedor = str(datosAlq[3])
            dnicli = str(datosAlq[4])
            nomecli = str(datosAlq[5]) + " " + str(datosAlq[6])
            idProp = str(datosAlq[7])
            tipoprop = str(datosAlq[8])
            precioAlq = datosAlq[9]
            precioAlqStr = f"{precioAlq:,.1f} €"
            localidad = datosAlq[10]
            dirProp = datosAlq[11]

            var.report.drawString(55, 690, "DATOS CLIENTE:")
            var.report.drawString(100, 670, "DNI: " + dnicli)
            var.report.drawString(330, 670, "Nombre: " + nomecli)

            var.report.drawString(55, 640, "DATOS CONTRATO:")
            var.report.drawString(100, 620, "Num de contrato: " + str(idAlquiler))
            var.report.drawString(100, 600, "Num de vendedor: " + idVendedor)
            var.report.drawString(330, 620, "Fecha de inicio: " + fechaini)
            var.report.drawString(330, 600, "Fecha de fin: " + fechafin)

            var.report.drawString(55, 570, "DATOS INMUEBLE:")
            var.report.drawString(100, 550, "Num de propiedad: " + idProp)
            var.report.drawString(100, 530, "Tipo de propiedad: " + tipoprop)
            var.report.drawString(330, 550, "Dirección: " + dirProp)
            var.report.drawString(330, 530, "Localidad: " + localidad)

            var.report.line(40, 500, 540, 500)
            var.report.drawString(55, 470, "Mensualidad correspondiente a:")
            var.report.setFont('Helvetica-Bold', size=12)
            datos_mensualidad = conexion.Conexion.datosOneMensualidad(idMensualidad)
            var.report.drawCentredString(300, 470, datos_mensualidad[1].upper())

            iva = precioAlq * 0.1
            total = precioAlq + iva

            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(370, 470, "Subtotal: ")
            var.report.drawRightString(540, 470, precioAlqStr)
            var.report.drawString(370, 450, "IVA (10%): ")
            var.report.drawRightString(540, 450, str(iva) + " €")
            var.report.setFont('Helvetica-Bold', size=12)
            var.report.drawString(370, 420, "Total: ")
            var.report.drawRightString(540, 420, str(total) + " €")
            var.report.line(40, 390, 540, 390)

            Informes.topInforme(titulo)
            Informes.footInforme(titulo, 1)

            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdffac):
                    os.startfile(pdf_path)

        except Exception as e:
            print("Error en reportReciboMes", str(e))
