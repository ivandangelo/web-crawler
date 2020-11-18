# *tp2-EDD-Python*
--------

## Nombres de los integrantes del Grupo: 

* Fernandez Lucas
* Ledesma Javier
* Ivan Manuel D'angelo

## Decisiones de disenio:

Elejimos usar la implementacion de un arbol B+ respetando el funcionamiento que vimos en clase al insertar y buscar, exceptuando que los nodos hojas no estan referenciados entre si, porque resuelve la busqueda con comodines, ya que al buscar las palabras que son
por poner un ejemplo de la forma algo* lo que hacemos es en el arbol localizar las palabras que empiezen con "algo" descartando las que son menor que "algo" y quedandonos con el hijo derecho donde las palabras de esos hijos seran mayor o igual que "algo".Una vez ubicadas nos traemos los links asociados a esas palabras con el metodo obtener_documentos. Como estructura para representar las palabras y la lista de links asociada a cada una usamos una 
clase PalabraDocumentos porque nos parecio la forma mas ordenada de representar la informacion, cada nodo esta representado por la clase BtreeNode que contiene una lista de objetos PalabraDocumentos. La estructura del arbol b+ esta representada por la clase BTree. Para separar las palabras y links usamos la libreria HTMLParser que nos recomendaron en la consigna del TP, debido a que ya nos venia dado. También en el grupo nos facilitaron la forma de poder descartar todo lo que no nos servía de este mismo.
En el modulo de WebCrawler decidimos resolver el tema de la "robustez" empleando una listas con los links que ya se han visitado asi evitamos caer en bucles. Con *response = urlopen(url_actual, timeout=self.Tmin)* se establece un parametro de tiempo maximo para visitar la url.
Para el modulo de Search decidimos que utilice un arbol b+ de orden 3 como atributo, donde en este se guardara la informacion extraida por el WebCrawler. Lo que hicimos fue pedir al usuario que ingrese las palabras a buscar, a medida que el usuario va ingresando la palabra o palabras a buscar se localizan en el arbol b+ con sus respectivos documentos y se le muestran al usuario, este mismo tiene la opcion de finalizar la busqueda o reiniciar el crawler para que siga buscando informacion.

## Descripcion de cada archivo:

__PalabraDocumentos.py__
Estructura que se encarga de almacenar cada palabra con su correspondiente lista de links, posee metodos sobreescritos para comparar los objetos por mayor o menor 
mediante sus palabras.

__BTreeNode.py__
Estructura que se encarga de representar cada nodo del arbol, los objetos de la lista "palabras" son de tipo PalabraDocumento,
Asi cada nodo tendra una lista de claves(palabras) con cada clave asociada a su valor(links), una lista de nodos hijos y una propiedad padre que hace referencia a su nodo padre.
Posee metodos que permiten consultar si una palabra se encuentra en el nodo,en caso de no encontrarse nos devuelve la posicion del nodo hijo en el que tendriamos que seguir buscando, tambien posee un metodo para encontrar el nodo hoja de una palabra en caso que la palabra este en el arbol.

__BTree.py__
Estructura que representa el Arbol b+ donde se almacenan las palabras y los links recolectados por el crawler,estos links forman el indice invertido para cada palabra y se almacenan en los nodos hojas. Respeta el funcionamiento del arbol b+ que vimos en clase. Inserta la palabra en el nodo donde corresponda y luego si es necesario, comienza a partir hacia arriba. Al realizar la insercion se filtra por STOP WORDS, palabras con logitud menor o igual a tres.
Se le puede asignar un orden especifico. Posee metodos para consultar si existe una palabra en el arbol y obtener los links asociados.

__Logger.py__
Registra los movimientos del crawler segun la zona horaria de BS AS, cuando se inicia, se interrumpe, visita una url, termina de ejecutarse, termina de visitar una url
de su frontera.Usamos la libreria configparser porque nos fue recomendada en la consigna del TP, usando esta libreria leyendo 'config.ini' se carga el archivo en donde se ira guardando los movimientos del crawler.


__Crawler.py__
Se extrae del archivo 'config.ini' mediante la libreria configparser la configuracion que el crawler debera respetar, es decir, las url de su frontera que debera visitar,y el tiempo minimo que debera respetar entre cada peticion al mismo servidor(en este caso, esos servidores seran los de untref y uba).
Extrae la informacion de la web para poder armar los indices y soportar el buscador,mediante la libreria de HTMLParser se separa esa informacion quedandose con los links y el texto de cada link,esto lo hacemos mediante la invocacion del metodo feed que a su vez ejecuta los eventos sobreescritos handle_data,handle_startendtag,handle_starttag descartando etiquetas y tabulaciones del HTML entre otras cosas, para esto aplicamos los conocimientos vistos en clase sobre expresiones regulares y normalizado de textos.
Se agrega cada palabra del texto al arbol b+ añadiendo el indice invertido para esa palabra en las hojas del arbol. El texto recolectado lo normaliza quitando acentos y remplazando mayusculas por minusculas.

__Search.py__
Esta clase se encarga de buscar las palabras que ingrese el usuario, con o sin comodines. Posee como atributo un arbol b+ de orden 3, el cual comparte con el Crawler y donde se almacenara la informacion extraida.Permite pausar el crawler o una vez buscadas las palabras que ingreso el usuario volver a iniciarlo.

## Conclusiones:
Con este trabajo practico entendimos mejor como funciona la estructura de datos del arbol b+ permitiendo realizar busquedas con prefijos o sufijos, ademas presenta ventajas al buscar debido que para cada clave, sus hijos izquierdos seran menor y los derechos mayor o iguales al padre, descartando en la busqueda "ramas" o "pedazos" del arbol y de este modo agilizandola. Ademas aplicamos los conocimientos aprendidos a la hora de construir un indice invertido, donde para cada palabra se realiza un filtrado y un normalizado de la misma.
Entendimos como funciona la estructura de un WebCrawler, y que con librerias como HTMLParser podemos separar contenido extraido por el crawler que no nos sirva como por ejemplo etiquetas,tags, tabulaciones, etc.
Profundizamos los conocimientos en el uso de expresiones regulares ya que nos ayudo a buscar patrones en el texto a la hora de en el crawling separar el contenido extraido mencionado anteriormente.