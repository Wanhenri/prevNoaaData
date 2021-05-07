"""Destinado para baixar aquivos do GFS week

GFS-week1-anom-01May2021-07May2021-made-on-20210501_float.zip.

USAGE:
    python prevNoaaData.py <URL>
"""

import requests
import datetime
import os.path
import time
import os
import itertools as it
from log import log,logerro
from zipfile import ZipFile
#import zipfile
import threading
from threading import Thread

from temporizador import IntervalRunner

#import pytz
from datetime import datetime, timezone, timedelta, date
from tzlocal import get_localzone

from descompactar import unzipefile

def convert_bytes(num):
    """Essa função converterá os byte para MB.... GB... etc

    Args:
        num: Valor de entrada do arquivo baixado.
    
    Returns:
        Retorna o arquivo de acordo com o tamanho que ele se enquadra

    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    """Essa função retornará o tamanho do arquivo já convertido

    Args:
        file_path: caminho do arquivo
    
    Returns:
        Tamanho do arquivo
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


dir_local = "H:\cemaden\Prev_NOAA_2021\GFS/"

class definirData:
    """ Classe destinada em separar a data inicial e data final

    Attributes 
        diaInicial: data inicial contendo um valor inteiro, por exemplo, 1.
        diaFinal: data final contendo um valor inteiro, por exmplo, 2.
    """
    def __init__(self,diaInicial, diaFinal):
        """
        Parameters
        ----------
        diaInicial : int
            Valor inicial da data
        diaFinal : int
            Valor final da data
        """
        self.diaI = diaInicial
        self.diaF = diaFinal

    def getStartDay(self):
        """Função retorna a data inicial

        Args:
            self: usará self.diaI
    
        Returns:
            retorna a data do dia no formato, por exemplo, 01May2021 
        """
        return (date.today() + timedelta(days=self.diaI)).strftime("%d%b%Y")
    
    def getEndDate(self):
        """Função retorna a data final

        Args:
            self: usará self.diaF
    
        Returns:
            retorna a data do dia no formato, por exemplo, 01May2021 
        """
        return (date.today() + timedelta(days=self.diaF)).strftime("%d%b%Y")
    
    def getStartDayMadeOn(self):
        """Função retorna a data final

        Args:
            self: usará self.diaI
    
        Returns:
            retorna a data do dia no formato, por exemplo, 20210430 
        """
        return (date.today() + timedelta(days=self.diaI)).strftime("%Y%m%d")

def automation(*args):
    """Responsável por baixar os arquivos, verificar seu tamanho, sua existencia e descompactar 
    """
    try:
        for a, b in zip(list(range(-4, 1, 1)), list(range(2, 10, 1))):
            Data = definirData(a, b)
            filename = "GFS-week1-anom-" + str(Data.getStartDay()) + "-" + str(Data.getEndDate()) + "-made-on-"+str(Data.getStartDayMadeOn())+"_float.zip"
            print(filename)

            """ Realizado a verificação da existencia dos dados
            Caso seja verificado sua existência, ele segue o programa para o inicio dele,
            porem, se não for verficado sua existência, ele segue adiante.
            """
            if os.path.exists(dir_local + filename) == True :
                print("File exist: ", filename)
            else:
                print("File not exist: ", filename)
                print("create: ", filename)

                """
                    Caminho dos dados juntamente com os métodos utilizados para manipulação de datas criado na 'class definirData' 
                """
                url = "https://ftp.cpc.ncep.noaa.gov/GIS/GRADS_GIS/GeoTIFF/PREC_FORECAST/GFS-week1-anom-" + str(Data.getStartDay()) + "-" + str(Data.getEndDate()) + "-made-on-"+str(Data.getStartDayMadeOn())+"_float.zip"

                r = requests.get(str(url))

                with open(dir_local + filename, 'wb') as f:
                    f.write(r.content)
                    print(os.path.exists(dir_local + filename))
                    sizeFile = file_size(dir_local + filename)
                    print(sizeFile)

                    time.sleep(1.4)

                    """Realizado uma verificação do tamanho do arquivo. Se for verificado uma inconsistencia nos dados, 
                    ele informatá o tamanho do arquivo, seu tamanho e salvará no logerro(), gerando o arquivo logerro.txt
                    """

                    if sizeFile < str(300):   

                        print("O arquivo existe, mas está corrompido. Olhar log")
                        logerro(filename,sizeFile)
                        continue

                    time.sleep(1.4)

                    print(os.path.exists(dir_local + filename))

                    """ Após baixado o arquivo, ocorrerá a descompactação dos dados dentro do mesmo local de dowload 
                    """

                    #https://programadorviking.com.br/python-zipfile/
                    #ZipExtract = ZipFile(dir_local + filename, 'r')
                    #ZipExtract.extractall(dir_local)
                    #ZipExtract.close()
                    path = os.path.join(dir_local, filename)
                    print(path)
                    zf = ZipFile(path, 'r')
                    zf.extractall(dir_local)
                    zf.close() # close file after extraction is completed'''
                    #permissao = 755
                    #os.chmod(filename,permissao)

                    """ Um arquivo de log é gerado com as informações necessárias sobre o arquivo baixado 
                    """
                    log(filename,sizeFile)
    
    except Exception as e:
        print(e)
        logerro(filename,sizeFile)    

#Rodando de tempo e tempo
interval_monitor = IntervalRunner(86400.0,automation)
interval_monitor.start()


threading.Event().wait()

 