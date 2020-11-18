import configparser, re
from BTreeNode import *
from PalabraDocumentos import PalabraDocumentos


class BTree(object):
    def __init__(self, orden):
        self.raiz = BTreeNode(True)
        self.orden = orden
        configuracion = configparser.ConfigParser()
        configuracion.read("config.ini")
        self.longitud_min = int(configuracion["INVERTED_INDEX"]["min_long"])

    '''
        Devuelve un listado de tuplas (palabra, documentos) con cada palabra matcheada por la busqueda
    '''
    def obtener_documentos(self, palabra):
        palabraDocumentos = []
        comodin = False

        if palabra.endswith('*'):
            comodin = True
            palabra = palabra.split('*')[0]

        # Me traigo el nodo con la clave por la que tengo que empezar a buscar
        encontrado, nodo = self.consultar_clave(PalabraDocumentos(palabra, []))
        if not encontrado:
            return []

        # Empiezo a buscar las hojas a partir de ese nodo y me guardo las palabras y documentos en donde la palabra matchee con la busqueda del usuario
        this_level = [nodo]
        while this_level:
            next_level = []
            for node in this_level:
                if node.hijos:
                    next_level.extend(node.hijos)
                elif node.esHoja:
                    palabrasDocumento = node.palabras
                    for palabraDocumento in palabrasDocumento:
                        if (comodin and palabraDocumento.palabra.startswith(palabra)) or (not comodin and palabraDocumento.palabra == palabra):
                            palabraDocumentos.append((palabraDocumento.palabra, palabraDocumento.paginas))
            this_level = next_level
        return palabraDocumentos

    '''
        Devuelve la primera clave en donde encuentra esa palabra
    '''
    def consultar_clave(self, palabra):
        nodo = self.raiz
        while True:
            encontrado, pos = nodo.consultar_clave(palabra)
            if encontrado:
                return (True, nodo)
            elif nodo.esHoja:
                return (False, nodo)
            else:
                nodo = nodo.hijos[pos]

    '''
        Consulta si existe la palabra en alguna hoja
    '''
    def consultar_hoja(self, palabra):
        nodo = self.raiz
        while True:
            encontrado, pos = nodo.consultar_hoja(palabra)
            if encontrado and nodo.esHoja:
                return (True, nodo)
            elif encontrado and not nodo.esHoja:
                nodo = nodo.hijos[pos + 1]
            elif nodo.esHoja:
                return (False, nodo)
            else:
                nodo = nodo.hijos[pos]

    def insertar(self, palabra):
        # Si la palabra es una stopword o no es mayor o igual a la longitud minima parametrizada, no se inserta.
        stopwords = ['un', 'una', 'unas', 'unos', 'uno', 'sobre', 'todo', 'también', 'tras', 'otro', 'algún', 'alguno', 'alguna', 'algunos',
                     'algunas', 'ser', 'es', 'soy', 'eres', 'somos', 'sois', 'estoy', 'esta', 'estamos', 'estais', 'estan', 'como', 'en',
                     'para', 'atras', 'porque', 'por qué', 'estado', 'estaba', 'ante', 'antes', 'siendo', 'ambos', 'pero', 'por', 'poder',
                     'puede', 'puedo', 'podemos', 'podeis', 'pueden', 'fui', 'fue', 'fuimos', 'fueron', 'hacer', 'hago', 'hace', 'hacemos',
                     'haceis', 'hacen', 'cada', 'fin', 'incluso', 'primero	desde', 'conseguir', 'consigo', 'consigue', 'consigues', 'conseguimos',
                     'consiguen', 'ir', 'voy', 'va', 'vamos', 'vais', 'van', 'vaya', 'gueno', 'ha', 'tener', 'tengo', 'tiene', 'tenemos', 'teneis',
                     'tienen', 'el', 'la', 'lo', 'las', 'los', 'su', 'aqui', 'mio', 'tuyo', 'ellos', 'ellas', 'nos', 'nosotros', 'vosotros', 'vosotras',
                     'si', 'dentro', 'solo', 'solamente', 'saber', 'sabes', 'sabe', 'sabemos', 'sabeis', 'saben', 'ultimo', 'largo', 'bastante', 'haces',
                     'muchos', 'aquellos', 'aquellas', 'sus', 'entonces', 'tiempo', 'verdad', 'verdadero', 'verdadera	cierto', 'ciertos',
                     'cierta', 'ciertas', 'intentar', 'intento', 'intenta', 'intentas', 'intentamos', 'intentais', 'intentan', 'dos', 'bajo',
                     'arriba', 'encima', 'usar', 'uso', 'usas', 'usa', 'usamos', 'usais', 'usan', 'emplear', 'empleo', 'empleas', 'emplean',
                     'ampleamos', 'empleais', 'valor', 'muy', 'era', 'eras', 'eramos', 'eran', 'modo', 'bien', 'cual', 'cuando', 'donde', 'mientras',
                     'quien', 'con', 'entre', 'sin', 'trabajo', 'trabajar', 'trabajas', 'trabaja', 'trabajamos', 'trabajais', 'trabajan', 'podria',
                     'podrias', 'podriamos', 'podrian', 'podriais', 'yo', 'aquel']
        if len(palabra.palabra) < self.longitud_min or not re.fullmatch(r'[a-záéíóúñ]+', palabra.palabra, re.IGNORECASE) or palabra.palabra in stopwords:
            return

        # Devuelve si la palabra ya fue insertada y el nodo donde se encuentra
        insertado, nodo = self.consultar_hoja(palabra)
        # Devuelve si se encuentra en el nodo y la posicion dentro del listado de palabras
        encontrado, pos = nodo.consultar_hoja(palabra)

        # Si fue insertado, itera por las paginas de la palabra a insertar 
        # Inserta cada pagina que no exista en la palabra ya insertada
        if insertado:
            for pagina in palabra.paginas:
                if pagina not in nodo.palabras[pos].paginas:
                    nodo.palabras[pos].paginas.append(pagina)
            return
        
        # Inserta siempre la palabra en el nodo 
        # correspondiente aunque ya esté lleno (luego se arregla al momento de splitear)
        nodo.palabras.insert(pos, palabra)
        # Splitea hacia arriba mientras el nodo supere la cantidad de palabras
        while len(nodo.palabras) == self.orden:
            # Asigna al padre del nodo en caso de que tenga, sino crea uno nuevo
            padre = nodo.padre if nodo.padre else BTreeNode()
            # Si el nodo actual es la raiz, pasa a ser raiz el nuevo padre.
            if nodo == self.raiz:
                self.raiz = padre
            posHijo = 0
            # Si el padre ya tiene este nodo en sus hijos, se trae la posicion del mismo
            if nodo in padre.hijos:
                posHijo = padre.hijos.index(nodo)
            # Sino, inserta el hijo en la posicion 0
            else:
                padre.hijos.insert(posHijo, nodo)
            # Separa los hijos en esa posición
            self._separar_hijos(padre, posHijo)
            # Setea al padre como el nodo para separar hacia arriba.
            nodo = padre

    def _separar_hijos(self, nodoPadre, pos_hijo):
        # Hijo "izquierdo"
        hijo = nodoPadre.hijos[pos_hijo]
        hijo.padre = nodoPadre
        # Nuevo hijo  que va a ser el "derecho"
        nuevohijo = BTreeNode(hijo.esHoja)
        nuevohijo.padre = nodoPadre
        orden = self.orden

        # Inserta el nuevo hijo a la derecha
        nodoPadre.hijos.insert(pos_hijo+1, nuevohijo)

        # Si el hijo es una hoja, pasa al padre sólo la palabra (clave)
        # if hijo.esHoja:
        nodoPadre.palabras.insert(pos_hijo, PalabraDocumentos(hijo.palabras[int((orden-1)/2)].palabra, []))
        # Sino, le pasa el objeto entero (que ya es sólo la palabra)
        # else:
        #     nodoPadre.palabras.insert(pos_hijo, hijo.palabras[int((orden-1)/2)])

        # Si el nuevo hijo es una hoja, sus palabras van a ser las del izquierdo desde la mitad en adelante
        if nuevohijo.esHoja:
            nuevohijo.palabras = hijo.palabras[int((orden-1)/2):]
        else:
        # Si no es una hoja, sus palabras van a ser desde las del izquierdo desde la mitad mas uno en adelante
            nuevohijo.palabras = hijo.palabras[int(((orden-1)/2) + 1):]
        # Las palabras del hijo izquierdo van a ser las mismas que tenía pero hasta la mitad
        hijo.palabras = hijo.palabras[:int((orden-1)/2)]

        # Separa los hijos en caso según si el arbol es de orden par o impar
        if not hijo.esHoja:
            if self.orden % 2 == 1:  # arbol de orden impar
                nuevohijo.hijos = hijo.hijos[int(orden/2+1):]
                hijo.hijos = hijo.hijos[:int(orden/2+1)]
            else:  # arbol de orden par
                nuevohijo.hijos = hijo.hijos[int(orden/2):]
                hijo.hijos = hijo.hijos[:int(orden/2)]
            # Arriba se separan los hijos pero los padres quedaban mal referenciados
            self._set_padre(nuevohijo)
            self._set_padre(hijo)

    def _set_padre(self, nodo):
        for hijo in nodo.hijos:
            hijo.padre = nodo

    def __str__(self):
        root = self.raiz
        return root.__str__() + '\n'.join([hijo.__str__() for hijo in root.hijos])

    def print_order(self):
        this_level = [self.raiz]
        while this_level:
            next_level = []
            output = ""
            for node in this_level:
                if node.hijos:
                    next_level.extend(node.hijos)
                output += str(node.palabras) + " "
            print(output)
            this_level = next_level
