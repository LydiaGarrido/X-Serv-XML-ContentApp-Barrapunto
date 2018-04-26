from django.shortcuts import render

# Create your views here.

from cms.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request

rss_contenido = ""

FORMULARIO = """
    <form method = 'POST'>
    <b>Nombre: </b><br>
    <input type='text' name='nombre'><br>
    <b>Pagina: </b><br>
    <input type='text' name='page'><br>
    <input type='submit' value='Enviar'></form>
"""

VOLVER = """
    <a href="http://localhost:8000/">
    Volver a la pagina principal</a>
"""

class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        global rss_contenido
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = "Title: " + self.theContent + "."
                print(self.title)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = " Link: " + self.theContent + "."
                rss_contenido += "<ul><li>"
                rss_contenido += "<a href=" + self.theContent + ">"
                rss_contenido += self.title + "</a><br>\n"
                rss_contenido += "</ul></li>"
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


def barra(request):
    content = Pages.objects.all()
    respuesta = "Bienvenido a cms Barrapunto<br>"
    respuesta += "<br>Páginas almacenadas:<br>"
    for pagina in content:
        respuesta += "<ul><li>" + pagina.name + " / " + pagina.page
        respuesta += "</ul></li>"
    return HttpResponse(respuesta)


@csrf_exempt
def pag(request, resource):
    if request.method == "GET":
        try:
            pagina = Pages.objects.get(name=resource)
            respuesta = pagina.page + "<br>"
            respuesta += "<br>Contenido de Barrapunto:<br>"
            respuesta += rss_contenido
        except Pages.DoesNotExist:
            respuesta = "La página no existe<p>"
            respuesta += "Rellene el siguiente formulario "
            respuesta += "si desea crearla:<p>"
            respuesta += FORMULARIO
    elif request.method == "POST":
        name = request.POST['nombre']
        page = request.POST['page']
        nueva_pag = Pages(name=name, page=page)
        nueva_pag.save()
        respuesta = "Pagina guardada "
        respuesta += VOLVER
    elif request.method == "PUT":
        try:
            pagina = Pages.objects.get(name=resource)
            respuesta = "La pagina ya está creada. "
            respuesta += VOLVER
        except Pages.DoesNotExist:
            page = request.body
            nueva_pag = Pages(name=resource, page=request.body)
            nueva_pag.save()
            respuesta = "Se ha guardado la pagina "
            respuesta += nueva_pag.name + ". " + VOLVER
    else:
        respuesta = "Metodo no permitido"
    return HttpResponse(respuesta)


def error(request):
    respuesta = "Ha ocurrido un error: "
    respuesta += "la pagina no esta disponible. "
    return HttpResponse(respuesta + VOLVER)


def update(request):
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    url = "http://barrapunto.com/index.rss"
    xmlFichero = urllib.request.urlopen(url)
    theParser.parse(xmlFichero)

    respuesta = "Titulares de barrapunto:<br>" + rss_contenido

    return HttpResponse(respuesta)
