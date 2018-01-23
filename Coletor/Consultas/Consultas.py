# -*- coding: utf-8 -*-
'''
Created on 24/01/2014

@author: raulc_000

Script que contem os códigos principais. A Thread principal e o programa principal.
Esses Scripts só funcionarão se os Orgão Superiores, Orgãos e Unidades Gestoras 
estiverem carregados no Banco de Dados

'''
import threading
import time
import psycopg2
import ConsultasAvancadas
from stem.control import Controller
 

#classe principal, em Thread, que realizar diversas consultas simultaneas ao portal da transparencia
class Consulta_Portal_Thread (threading.Thread):
    
    BASE_URL = 'http://www.portaltransparencia.gov.br/despesasdiarias/resultado?consulta=avancada'
    PERIODO_INICIO = '&periodoInicio='
    DIA_INICIO = 25
    MES_INICIO = 05
    ANO = 2010
    PERIODO_INICIO_VALOR = str(DIA_INICIO) + '%2F' + str(MES_INICIO) + '%2F' + str(ANO)
    PERIODO_FIM = '&periodoFim='
    DIA_FIM = 26
    MES_FIM = 05
    ANO_FIM = 2014
    PERIODO_FIM_VALOR = str(DIA_FIM) + '%2F' + str(MES_FIM) + '%2F' + str(ANO)
    FASE = '&fase='
    FASE_VALOR = 'EMP'
    CODIGO_OS = '&codigoOS=' 
    CODIGO_OS_VALOR = ''
    CODIGO_ORGAO = '&codigoOrgao='
    CODIGO_ORGAO_VALOR = ''
    CODIGO_UG = '&codigoUG='
    CODIGO_UG_VALOR = ''
    CODIGO_ED = '&codigoED='
    CODIGO_ED_VALOR = 'TOD'
    CODIGO_FAVORECIADO = '&codigoFavorecido='
    SEARCH_URL = BASE_URL + PERIODO_INICIO + PERIODO_INICIO_VALOR + PERIODO_FIM + PERIODO_FIM_VALOR + FASE + FASE_VALOR + CODIGO_OS + CODIGO_OS_VALOR
    controller = None
    consultaAvcF = None
    
    def __init__(self, threadID, name, d_inic, m_inic, ano, d_fim, m_fim, ano_fim, controller):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.DIA_INICIO = d_inic
        self.MES_INICIO = m_inic
        self.ANO = ano
        self.PERIODO_INICIO_VALOR = "{0:0=2d}".format(self.DIA_INICIO) + '%2F' + "{0:0=2d}".format(self.MES_INICIO) + '%2F' + "{0:0=2d}".format(self.ANO)
        self.DIA_FIM = d_fim
        self.MES_FIM = m_fim
        self.ANO_FIM = ano_fim
        self.PERIODO_FIM_VALOR = "{0:0=2d}".format(self.DIA_FIM) + '%2F' + "{0:0=2d}".format(self.MES_FIM) + '%2F' + "{0:0=2d}".format(self.ANO)   
        
        conn_string = "host='193.169.1.8' dbname='portaltransparencia' user='postgres' password='senha'"
        
        conn = psycopg2.connect(conn_string)
        
        cursor = conn.cursor()
        
        stringSQL = "Select data, ultimo_codigo_os, ultimo_codigo_orgao, ultimo_codigo_ug from consulta_realizada WHERE data= '" + "{0:0=2d}".format(self.DIA_INICIO)
        stringSQL =  stringSQL + '/' + "{0:0=2d}".format(self.MES_INICIO) + '/' + "{0:0=2d}".format(self.ANO) + "' and doing != '0'" 
        
        cursor.execute(stringSQL) 

        rows = cursor.fetchone()
        
        if (rows is None) or (rows[1] == '' and rows[2 ] == '' and rows[3] == ''):
            
            stringSQL = "INSERT INTO consulta_realizada (data, doing) VALUES('" + "{0:0=2d}".format(self.DIA_INICIO) 
            stringSQL =  stringSQL + '/' + "{0:0=2d}".format(self.MES_INICIO) + '/' + "{0:0=2d}".format(self.ANO)
            stringSQL =  stringSQL + "', '1')"
                    
            cursor.execute(stringSQL) 
            conn.commit()
            
            conn.close()
            
            nao_cria = 0
        else :
            self.CODIGO_OS_VALOR = rows[1]
            self.CODIGO_ORGAO_VALOR = rows[2]
            self.CODIGO_UG_VALOR = rows[3]
            
            nao_cria = 1
            
        self.controller = controller
        
        threadLock.acquire()
        print_time(self.name)        
        self.consultaAvcF = ConsultasAvancadas.Consulta_Favorecido("{0:0=2d}".format(self.DIA_INICIO), "{0:0=2d}".format(self.MES_INICIO), "{0:0=2d}".format(self.ANO) , self.SEARCH_URL, self.controller, nao_cria)
        threadLock.release()

    def setParam(self, d_inic, m_inic, ano, d_fim, m_fim, ano_fim ):
        self.DIA_INICIO = d_inic
        self.MES_INICIO = m_inic
        self.ANO = ano
        self.PERIODO_INICIO_VALOR = "{0:0=2d}".format(self.DIA_INICIO) + '%2F' + "{0:0=2d}".format(self.MES_INICIO) + '%2F' + "{0:0=2d}".format(self.ANO)
        self.DIA_FIM = d_fim
        self.MES_FIM = m_fim
        self.ANO_FIM = ano_fim
        self.PERIODO_FIM_VALOR = "{0:0=2d}".format(self.DIA_FIM) + '%2F' + "{0:0=2d}".format(self.MES_FIM) + '%2F' + "{0:0=2d}".format(self.ANO)   

    def run(self):
        print "Starting " + self.name
        
        conn_string = "host='193.169.1.8' dbname='portaltransparencia' user='postgres' password=senha'"
        
        conn = psycopg2.connect(conn_string)
        
        cursor = conn.cursor()
        
        stringSQL = " select codigo_os, codigo_orgao, codigo from unidade_gestora order by codigo_os, codigo_orgao;"
        
        cursor.execute(stringSQL)
        
        rows = cursor.fetchall()
        
        list = None
             
        entrou = 0
        for row in rows:
            if (self.CODIGO_OS_VALOR <> '' and self.CODIGO_ORGAO_VALOR <> '' and self.CODIGO_UG_VALOR <> '') or (self.CODIGO_OS_VALOR is None and self.CODIGO_ORGAO_VALOR is None and self.CODIGO_UG_VALOR is None ):
                if  (self.CODIGO_OS_VALOR == str(row[0]) and self.CODIGO_ORGAO_VALOR == str(row[1]) and self.CODIGO_UG_VALOR == str(row[2])) or entrou == 1:
                    entrou = 1
                else :
                    continue
                    
            threadLock.acquire()
            
            print_time(self.name)
            
            self.SEARCH_URL = self.BASE_URL + self.PERIODO_INICIO + self.PERIODO_INICIO_VALOR + self.PERIODO_FIM + self.PERIODO_FIM_VALOR + self.FASE + self.FASE_VALOR + self.CODIGO_OS + str(row[0]) + self.CODIGO_ORGAO + str(row[1])
            self.SEARCH_URL = self.SEARCH_URL + self.CODIGO_UG + str(row[2]) + self.CODIGO_ED + str(52)

            lista = self.consultaAvcF.executa(self.SEARCH_URL)
                            
            threadLock.release()
            
            if len(lista) > 3:
                print lista
            
                item = 3
                while item < len(lista):
                    stringSQL = 'INSERT INTO consulta VALUES(' + str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) 
                    stringSQL =  stringSQL + ",'" + self.SEARCH_URL + "','" + lista[item] + "','" + lista[item + 1] 
                    stringSQL =  stringSQL + "','" + lista[item + 2] + "','" + "{0:0=2d}".format(self.DIA_INICIO) 
                    stringSQL =  stringSQL + '/' + "{0:0=2d}".format(self.MES_INICIO) + '/' + "{0:0=2d}".format(self.ANO) 
                    stringSQL =  stringSQL + "','" + "{0:0=2d}".format(self.DIA_FIM) + '/' + "{0:0=2d}".format(self.MES_FIM) 
                    stringSQL =  stringSQL + '/' + "{0:0=2d}".format(self.ANO) + "');"
                    item = item + 3
                
                    print stringSQL
                    cursor.execute(stringSQL)
                    conn.commit()
        
            stringSQL = "UPDATE consulta_realizada   SET ultimo_codigo_OS= '" + str(row[0]) + "', ultimo_codigo_ORGAO= '" + str(row[1]) 
            stringSQL =  stringSQL + "', ultimo_codigo_UG= '" + str(row[2]) + "' " + "WHERE data= '" + "{0:0=2d}".format(self.DIA_INICIO)
            stringSQL =  stringSQL + '/' + "{0:0=2d}".format(self.MES_INICIO) + '/' + "{0:0=2d}".format(self.ANO) + "'" 
    
        
            cursor.execute(stringSQL)
            conn.commit()
                
        stringSQL = "UPDATE consulta_realizada   SET doing='0' WHERE data= '" + "{0:0=2d}".format(self.DIA_INICIO)
        stringSQL =  stringSQL + '/' + "{0:0=2d}".format(self.MES_INICIO) + '/' + "{0:0=2d}".format(self.ANO) + "'" 

    
        print stringSQL
        cursor.execute(stringSQL)
        conn.commit()
    
        print "FIM!!!" + self.name
        
        conn.close()

def print_time(threadName):
    print "%s: %s" % (threadName, time.ctime(time.time()))


##########################################################
#                                                        #
#                 Programa principal                     #
# executa diversar Threads que realizam consultas no     #
# Portal da Transparência. As Threads coletam informações#
# de entidades públicas que realizam gastos em TI e os   #
# Favorecidos das respectivas Ordens Bancárias           #
#                                                        #
##########################################################
	

DIA_INICIO = 01 
DIA_FIM = 02
MES_INICIO = 01
MES_FIM = 01
ANO = 2014
ANO_FIM = 2014
thread = []

controller = Controller.from_port() 
controller.authenticate('123456')
# controller = None

threadLock = threading.Lock()
threads = []

conn_string = "host='193.169.1.8' dbname='portaltransparencia' user='postgres' password='senha'"

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()
  

#stringSQL = "select min(data) from consulta_realizada where done='1';"

#cursor.execute(stringSQL)

#rows = cursor.fetchall()

#if rows[0][0] is not None:
    
#    print str(rows[0][0].day) + "/" + str(rows[0][0].month) + "/" + str(rows[0][0].year)
    
#    DIA_INICIO = rows[0][0].day 
#    DIA_FIM = DIA_INICIO + 1
#    MES_INICIO = rows[0][0].month
#    MES_FIM = MES_INICIO
#    ANO = rows[0][0].year

#Consulta varios anos
while ANO <= ANO_FIM :
    item = 0
    while item < 16 :
        #Criar Thread
        thread.append(myThread(item, "Thread-" + str(item), DIA_INICIO, MES_INICIO, ANO, DIA_FIM, MES_FIM, ANO, controller))
          
        #Inicia a Thread da lista
        thread[item].start()
          
        #Adiciona Thread na lista
        threads.append(thread[item])
  
     
        if DIA_INICIO < 30 :
            DIA_INICIO = DIA_INICIO + 01
        else :
            DIA_INICIO = 01
            if MES_INICIO < 12 :
                MES_INICIO = MES_INICIO + 1
            else :
                MES_INICIO = 01
                if ANO < ANO_FIM :
                    ANO = ANO + 01  
          
        DIA_FIM = DIA_INICIO + 01 
        MES_FIM = MES_INICIO
          
        item = item + 1
      
    #Aguarda conclusão das Threads
    for t in threads:
        t.join()

# ConsultasAvancadas.newID(controller)
# 
# 
# DIA_INICIO = 9
# MES_INICIO = 6
# ANO = 2010
# DIA_FIM = 10
# MES_FIM = 06
# 
# controller = None
# 
# threadLock = threading.Lock()
# threads = []
# 
# #colocar ultima consulta
#   
# thread = myThread(0, "Thread-0", DIA_INICIO, MES_INICIO, ANO, DIA_FIM, MES_FIM, ANO, controller)
#    
# # Start new Threads
# thread.start()
# #thread[item].start()
#    
# # Add threads to thread list
# threads.append(thread)
# #threads.append(thread[item])
#    
# # Wait for all threads to complete
# for t in threads:
#     t.join()
#controller.close()

print "Exiting Main Thread"