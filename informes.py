from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.graphics import renderPM
import os
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
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado clientes"
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)
            items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 650, str(items[0]))
            var.report.drawString(100, 650, str(items[1]))
            var.report.drawString(190, 650, str(items[2]))
            var.report.drawString(285, 650, str(items[3]))
            var.report.drawString(360, 650, str(items[4]))
            var.report.drawString(450, 650, str(items[5]))
            var.report.line(50, 645, 525, 645)
            query = QtSql.QSqlQuery()
            query.prepare('select dnicli, apelcli, nomecli, movilcli, provcli, municli from clientes order by apelcli')
            if query.exec():
                x = 55
                y = 635
                while query.next():
                    if y <= 95:
                        var.report.setFont('Helvetica-Oblique', size=9)
                        var.report.drawString(450,90, "Página siguiente...")
                        var.report.showPage() #Crea una pág nueva
                        Informes.footInforme(titulo)
                        Informes.topInforme(titulo)
                        items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
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
                    dni = "***"+ str(query.value(0)[4:7]+"***")
                    var.report.drawCentredString(x + 10, y , str(dni))
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

    @staticmethod
    def reportPropiedades(self):
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today()
            fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
            nompdfprop = fecha + "_listadopropiedades.pdf"
            pdf_path = os.path.join(rootPath, nompdfprop)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado propiedades"
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)
            items = ['REF', 'TIPO', 'DIRECCIÓN', 'PROVINCIA', 'MUNICIPIO', 'HABITACIONES', 'PRECIO']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 650, str(items[0]))
            var.report.drawString(100, 650, str(items[1]))
            var.report.drawString(140, 650, str(items[2]))
            var.report.drawString(225, 650, str(items[3]))
            var.report.drawString(300, 650, str(items[4]))
            var.report.drawString(375, 650, str(items[5]))
            var.report.drawString(475, 650, str(items[6]))
            var.report.line(50, 645, 525, 645)
            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nompdfprop):
                    os.startfile(pdf_path)

        except Exception as e:
            print(e)

    def footInforme(titulo):
        try:
            total_pages = 0
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber()))

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
                var.report.drawString(230, 670, titulo)
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