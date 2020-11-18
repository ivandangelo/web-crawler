class BTreeNode(object):

    def __init__(self, hoja=False):
        self.esHoja = hoja
        self.palabras = []
        self.hijos = []
        self.padre = None

    '''
        Devuelve la primera aparicion de la palabra
    '''
    def consultar_clave(self, palabra):
        pos = 0
        while pos < len(self.palabras):
            if self.palabras[pos].palabra.startswith(palabra.palabra):
                return (True, pos)
            elif self.palabras[pos] < palabra:
                pos += 1
            else:
                break
        return (False, pos)

    '''
        Devuelve la hoja en donde aparece la palabra
    '''
    def consultar_hoja(self, palabra):
        pos = 0
        while pos < len(self.palabras):
            if self.palabras[pos] == palabra:
                return (True, pos)
            elif self.palabras[pos] < palabra:
                pos += 1
            else:
                break
        return (False, pos)

    def __str__(self):
        if self.esHoja:
            return "hoja BTreeNode with {0} claves\n\tPalabras:{1}\n\thijos:{2}\n".format(len(self.palabras), self.palabras, self.hijos)
        else:
            return "Internal BTreeNode with {0} claves, {1} hijos\n\tPalabras:{2}\n\n".format(len(self.palabras), len(self.hijos), self.palabras).join([hijo.__str__() for hijo in self.hijos])
