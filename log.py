 # -*- coding: utf-8 -*-
import datetime

def log(name,size):
    datainicio = datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')
    arquivo = open('logcoleta.txt','a')
    arquivo.write("******** \n")
    arquivo.write("Coleta de dado: \n")
    arquivo.write(str(datainicio) + "\n")
    arquivo.write(str(name) + "\n")
    arquivo.write("Size file: " + str(size) + "\n")
    arquivo.write("******** \n")
    arquivo.close()

def logerro(name,size):
    datainicio = datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')
    arquivo = open('logerro.txt','a')
    arquivo.write("******** \n")
    arquivo.write("Erro na coleta: \n")
    arquivo.write(str(datainicio) + "\n")
    arquivo.write(str(name) + "\n")
    arquivo.write("Size file: " + str(size) + "\n")
    arquivo.write("******** \n")
    arquivo.close()