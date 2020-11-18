import configparser
import socket
#from nltk.stem import PorterStemmer # pip install -U nltk
#from nltk.tokenize import word_tokenize
import re
from html.parser import HTMLParser
from urllib import parse
from urllib import error
from urllib.request import urlopen
from PalabraDocumentos import PalabraDocumentos

from Logger import Logger


class Crawler(HTMLParser):

    links=[]
    linksVisitados = []
    __text = []

    def __init__(self, bTree):
        HTMLParser.__init__(self)
        configuracion = configparser.ConfigParser()
        configuracion.read("config.ini")
        self.urls = configuracion["CRAWLER"]["URLs"].split(' ; ')
        self.Tmin = int(configuracion["CRAWLER"]["Tmin"])
        self.arbolB = bTree
        

    def iniciar(self):
        Logger.log('Crawler iniciado')
        for url in self.urls:
            try:
                self.fetch_page(url)
            except KeyboardInterrupt:
                break

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    value = self.replace_accents(value)
                    newURL=parse.urljoin(self.baseURL, value)
                    # Si el link no esta en la lista de links visitados ni en la de links x visitar, se agrega al listado
                    if newURL not in self.linksVisitados and newURL not in self.links and '#' not in newURL and ' ' not in newURL and newURL.startswith(self.baseURL):
                        self.links.append(newURL)
        elif tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    '''
        Elimina los acentos (usado para las URLs, sino no las puede abrir)
    '''
    def replace_accents(self, cadena):
        acentos = ['Á', 'É', 'Í', 'Ó', 'Ú', 'á', 'é', 'í', 'ó', 'ú']
        letras_normalizadas = ['A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']

        cadena_normalizada = cadena

        for letra in cadena:
            if letra in acentos:
                cadena_normalizada = cadena_normalizada.replace(letra, letras_normalizadas[acentos.index(letra)])
        return cadena_normalizada

    '''
        Se queda sólo con el texto plano del HTML
    '''
    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0 and not (self.lasttag == 'script' or self.lasttag == 'style'): # or self.lasttag == 'a'
            text = re.sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    '''
        Devuelve sólo el texto extraído del HTML
    '''
    def text(self):
        texto = ''.join(self.__text).strip()
        texto = texto.replace('\n', "")
        self.__text.clear()
        return texto
            
    def fetch_page(self, url):
        if (url not in self.linksVisitados):
            self.links.append(url)
        self.baseURL = url
        while any(self.links):
            url_actual = self.links[0]
            try:
                Logger.log(url_actual)
                self.linksVisitados.append(url_actual)
                response = urlopen(url_actual, timeout=self.Tmin)
                content_type = response.getheader('Content-type')
                if 'text/html' in content_type:
                    encoding=response.headers.get_param('charset')
                    data=response.read()
                    html_string=data.decode(encoding)
                    self.feed(html_string)
                palabras = self.text()
                # ps = PorterStemmer()
                # words = []
                # for palabra in word_tokenize(palabras, 'spanish'):
                #     words.append(ps.stem(palabra))
                # self.agregarPalabras(words, url_actual)
                self.agregarPalabras(palabras, url_actual)
                self.links.remove(url_actual)
            except error.URLError:
                self.links.remove(url_actual)
                Logger.log("URLError")
            except socket.timeout:
                Logger.log("Timeout")
                self.links.remove(url_actual)
            except KeyboardInterrupt:
                Logger.log("KeyboardInterrupt")
                raise
                # opcion = 0
                # while opcion not in [1,2]:
                #     opcion = int(input("1- Reanudar crawler\n"+
                #            "2- Salir\n"))
                
                #     if opcion == 1:
                #         continue
                    
                #     elif opcion == 2:
                #         self.links.clear()
                #         Logger.log("KeyboardInterrupt")
                #         break
                
        Logger.log(self.baseURL + ' completa')
        Logger.log('Crawler finalizado')

    '''
        Agrega las palabras del texto en el Arbol B
    '''
    def agregarPalabras(self, palabras, url):
        for palabra in palabras.split():
            self.arbolB.insertar(PalabraDocumentos(palabra.lower(), [url]))

