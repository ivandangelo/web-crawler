class PalabraDocumentos():

    def __init__(self, palabra, paginas):
        self.palabra = palabra
        self.paginas = paginas

    def __gt__(self, obj):
        return self.palabra > obj.palabra

    def __ge__(self, obj):
        return self.palabra >= obj.palabra

    def __lt__(self, obj):
        return self.palabra < obj.palabra

    def __le__(self, obj):
        return self.palabra <= obj.palabra

    def __eq__(self, obj):
        return self.palabra == obj.palabra

    def __repr__(self):
        return str((self.palabra, self.paginas))
    