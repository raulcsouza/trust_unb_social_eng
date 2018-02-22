# -*- coding: utf-8 -*-
'''
Created on 24/01/2014

@author: raulc_000
'''
#importa bibliotecas
import urllib2
from bs4 import BeautifulSoup as bs_parse
from mechanize import Browser
import socks
import socket
from stem import Signal
from stem.control import Controller
import time
import random
import re
import sys
import logging, logging.handlers
from unicodedata import normalize
from idlelib.ReplaceDialog import replace


#########################################################
#                                                       #
# Funções auxiliares e classe de consulta à Favorecidos #
#                                                       #
#########################################################

#remoção de acentos para facilitar idendificação do token
def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('utf-8','ignore')

#utiliza rede tor
def create_connection( address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

#log em arquivo texto
def gravalog(self, log):
    try :
        self.f.write(log + "\n")
        self.f.flush()
    except Exception, e:
        print "Problemas ao gravar no arquivo: ", str(e)
        print "\n log: " + str(log)
        sys.exit()

#troca endereço IP
def newID(self, controller):
    try :
        controller.signal(Signal.NEWNYM)
        aux = urllib2.urlopen("http://www.ifconfig.me/ip").read()
        print(aux)
        gravalog(self , aux + "\n")
        return aux
    except :
        time.sleep(random.choice(range(8,10)))
        controller.signal(Signal.NEWNYM)
        aux = urllib2.urlopen("http://www.ifconfig.me/ip").read()
        print(aux)
        gravalog(self , aux + "\n")
        return aux


#classe que realiza a consulta do favorecido
#busca algum favorecido com token relacionado ao tema informática, tecnologia da informação, etc
#geralmente na observação do registro no portal da transparencia encontra-se o objeto de contratação
class Consulta_Favorecido ():

    #atributos
    controller = None
    SEARCH_URL = None
    tor_control_hostname = "127.0.0.1"
    tor_control_port = "8118"
    tor_control_password = "123456"
    contador = 0
    ID = ""
    ver = "4"
    arquivo = ''
    f = None

    #construtor
    def __init__(self, d_inic, m_inic, ano, search_url, controller, nao_cria):
        arquivo = '//home//raul//Documents//unb_python//data//data' + str(d_inic) + "-" + str(m_inic) + "-" + str(ano) + '.txt'
        if nao_cria == 1:
            self.f = open(arquivo,'a')
        else :
            self.f = open(arquivo,'w')

        Consulta.controller = controller

        self.SEARCH_URL = search_url

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

        #abre conector na rede tor
        try:
            socket.socket = socks.socksocket
            socket.create_connection = create_connection
        except:
            print "problema ao abrir socket na rede tor"

        br = Browser()

        #prepara para iniciar consultas
        print "################### Consulta Avancada Portal Transparencia ###################"
        gravalog(self,"\n\n\n################### Consulta Avancada Portal Transparencia ###################\n\n")
        print "################### versao" + self.ver + " ###################"
        gravalog(self,"\n################### versao " + self.ver + " ###################\n\n")

        try :
            LRequest = urllib2.Request(SEARCH_URL," " )
            LResponse = br.open(LRequest)
            page = bs_parse(LResponse.read())
            print SEARCH_URL
            print page
            #f.write(page)
        except :
            print "problema ao realizar primeira consulta na web"

        gravalog(self,(page.text).encode('utf-8', 'ignore'))

        br.close()

        #Consulta.ID = newID(self, Consulta.controller)
        Consulta.ID = 000000000

        #Objeto para captura de logs.
        x = logging.getLogger("logarqui")
        x.setLevel(logging.DEBUG)

        #captura logs e grava em arquivo.
        h1 = logging.FileHandler("//home//raul//Documents//unb_python//data//log//erros" + str(d_inic) + "-" + str(m_inic) + "-" + str(ano) + '.log')
        f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
        h1.setFormatter(f)
        h1.setLevel(logging.DEBUG)
        x.addHandler(h1)

    def _del_ (self):
        gravalog(self,"FIM!!!")
        self.f.close()


    #metodo que encontra o Favoreciado
    def executa(self, search_url) :

        self.SEARCH_URL = search_url

        list = None
        list = [u'Favorecido:' , u'Valor:' , u'Observação do Documento:']

        socket.socket = socks.socksocket
        socket.create_connection = create_connection
        br = Browser()
        print search_url
        print "ID = " + str(Consulta.ID)
        gravalog(self,search_url + " cont = " + str(Consulta.ID) + "\n")
        LRequest = urllib2.Request(search_url," " )
        LResponse = br.open(LRequest)
        page = bs_parse(LResponse.read())

        #pode ir para fora!!!!

        soup = bs_parse(LResponse.get_data())
        img_captcha = soup.find('img', alt='captcha')
        if img_captcha != None :
            #caso encontre um captcha, o sistema troca o endereço IP
            try:
                print "CAPTCHA!!!"
                gravalog(self,"CAPTCHA\n")
            finally:
                Consulta.ID = newID(self, Consulta.controller)
                br.close()
                socket.socket = socks.socksocket
                socket.create_connection = self.create_connection
                br = Browser()
                print search_url + " cont = " + str(Consulta.ID)
                gravalog(self,search_url + " cont = " + str(Consulta.ID) + "\n")
                LRequest = urllib2.Request(search_url," " )
                LResponse = br.open(LRequest)
                page = bs_parse(LResponse.read())
        entra = 0

        #navega na página HTML consultando o Favorecido no link do hypertexto
        for table in page.findAll("table"):
            for row2 in table.findAll('tr'):
    #             print row2
                for col in row2.findAll('td'):
                    for href in col.findAll('a'):
                            print href
                            gravalog(self,str(href).encode('utf-8', 'ignore') + '\n')
                            #resp = br.follow_link(text_regex=href.string)
                            #html = resp.read()
                            #print html
                    if col.string != None :
                        m = re.search('a href', col.string)
                        if m != None :
                            print 'Link!!!'
                            gravalog(self,'Link!!!\n')
                            print col.string
                            gravalog(self,str(col.string).encode('utf-8', 'ignore') + '\n')
                        m = re.search('INFORMATICA', col.string)
                        if m != None :
                            entra = 1
                        m = re.search('TECNOLOGIA DA INFORMACAO', col.string)
                        if m != None :
                            entra = 1
                        m = re.search('TELECOMUNICACOES', col.string)
                        if m != None :
                            entra = 1
                        m = re.search('TELECOMUNICACAO', col.string)
                        if m != None :
                            entra = 1
                        m = re.search('NETWORKS', col.string)
                        if m != None :
                            entra = 1
                        m = re.search('NETWORK', col.string)
                        if m != None :
                            entra = 1
                        m = re.search('REDE', col.string)
                        if m != None :
                            entra = 1
                        m = re.search('REDES', col.string)
                        if m != None :
                            entra = 1
                        if entra == 1 :
                            logarqui = logging.getLogger("logarqui")
                            logarqui.debug("Inside f!")
                            try :
                                print 'BINGO!'
                                gravalog(self,'BINGO!\n')
                                print href.string
                                gravalog(self,str(href.string).encode('utf-8', 'ignore') + '\n')
                                LResponse = br.follow_link(text_regex= href.string)
                                html = LResponse.read()
                                print html
                                gravalog(self,html + '\n')
                                page = bs_parse(html)
                                cont = 3
                                for table in page.findAll("table"):
                                    for row2 in table.findAll('tr'):
                                        #             print row2
                                        favorecido = 0
                                        valor = 0
                                        observacao = 0
                                        for col in row2.findAll('td'):
                                            if favorecido == 1 :
                                                texto = str(col.string).decode('utf8').encode('utf8', 'ignore').replace("'", "").replace(";", "").replace("--", "")
                                                print texto
                                                gravalog(self,texto + '\n')
                                                list.append(texto)
                                            if valor == 1 :
                                                texto = str(col.string).decode('utf8').encode('utf8', 'ignore').replace("'", "").replace(";", "").replace("--", "")
                                                print texto
                                                gravalog(self,texto + '\n')
                                                list.append(texto)
                                            if observacao == 1 :
                                                texto = str(col.string).decode('utf8').encode('utf8', 'ignore').replace("'", "").replace(";", "").replace("--", "")
                                                print texto
                                                gravalog(self,texto + '\n')
                                                list.append(texto)
                                                print list
                                            if col.string != None :
                                                m = re.search(u'Favorecido:' , col.string)
                                                if m != None :
                                                    print u'Favorecido:'
                                                    gravalog(self, u'Favorecido:' )
                                                    favorecido = 1
                                                m = re.search(u'Valor:' , col.string)
                                                if m != None :
                                                    print u'Valor:'
                                                    gravalog(self, u'Valor:' )
                                                    valor = 1
                                                m = re.search(u'Observação do Documento:' , col.string)
                                                if m != None :
                                                    print u'Observação do Documento:'
                                                    gravalog(self, 'Observação do Documento:' )
                                                    observacao = 1

                                entra = 0
                                br.back()
                            except Exception, ex:

                                logarqui.exception
                                logarqui.error
                                logarqui.exception("\nProvlema na gravação de logs! \n" + search_url)

                            logarqui.debug("Finishing f!")
                                #sys.exitPortalTranspareciaef)
                                #print col.string
                                #print col
                                #print row2

        if len(list) != 0 :
            while len(list) % 3 != 0 :
                list.append(' ')
        br.close()
        return list
#         except :
#             print Exception
#             print 'problema com : ' + search_url
#             sys.exitPortalTransparecia
