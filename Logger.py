import configparser
from datetime import datetime
from pytz import timezone # pip install pytz
import os

class Logger():

    @staticmethod
    def log(mensaje):
        configuracion = configparser.ConfigParser()
        configuracion.read("config.ini")
        logPath = configuracion["CRAWLER"]["Log"]

        mensaje_logueo = "{} [{}]{}".format(mensaje, datetime.now(timezone('America/Argentina/Buenos_Aires')).strftime('%d/%m/%Y %H:%M:%S'), os.linesep)
        with (open(logPath, 'a')) as f:
            f.write(mensaje_logueo)