from Crawler import Crawler
from BTree import BTree
#from nltk.stem import PorterStemmer

class Search():

    def __init__(self):
        self.arbolB = BTree(3)
        self.crawler = Crawler(self.arbolB)
        self.iniciar_crawler()

    def pedir_ingreso(self):
        return input("Ingrese las palabras que desea buscar: (Ingrese 'F' para terminar la búsqueda o 'R' para reiniciar el crawler.)\n")

    def buscar(self):
        ingreso = self.pedir_ingreso()
        # ps = PorterStemmer()
        while not ingreso.lower() == 'f':
            if ingreso.lower() == 'r':
                break
            
            palabras = ingreso.split()
            for palabra in palabras:
                self.mostrar_paginas(palabra, self.buscar_palabra(palabra))
                # self.mostrar_paginas(palabra, self.buscar_palabra(ps.stem(palabra)))
            ingreso = self.pedir_ingreso()
        if ingreso.lower() == 'r':
            self.iniciar_crawler()

    '''
        Recibe una cadena a buscar en las palabras
        devueltas por el Crawler y devuelve las palabras
        encontradas con su pagina correspondiente
    '''
    def buscar_palabra(self, palabra):
        palabraDocumentos = self.arbolB.obtener_documentos(palabra)
        return palabraDocumentos

    def mostrar_paginas(self, palabra, pagina):
        print((palabra, pagina))

    def iniciar_crawler(self):
        print("Crawler iniciado, para interrumpirlo presione Ctrl + C \n")
        self.crawler.iniciar()
        self.buscar()
        


if __name__ == '__main__':
    Search()
