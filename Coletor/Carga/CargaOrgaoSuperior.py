'''
Created on 16/06/2013

@author: raulc_000

Script que captura todos os Orgãos Superiores do Governo presentes no Portal da Transparência
'''
#importa bibliotecas
import urllib ,urllib2
import psycopg2
from BeautifulSoup import BeautifulSoup as bs_parse
from mechanize import Browser

#inicialização de variáveis
BASE_URL = 'http://www.portaltransparencia.gov.br/despesasdiarias/resultado?consulta=avancada'
PERIODO_INICIO = '&periodoInicio='
PERIODO_INICIO_VALOR = '19%2F10%2F2010'
PERIODO_FIM = '&periodoFim='
PERIODO_FIM_VALOR = '18%2F11%2F2010'
FASE = '&fase='
FASE_VALOR = 'EMP'
CODIGO_OS = '&codigoOS=' 
CODIGO_OS_VALOR = '22000'
CODIGO_ORGAO = '&codigoOrgao='
CODIGO_UG = '&codigoUG='
CODIGO_UG_VALOR = 'TOD'
CODIGO_ED = '&codigoED='
CODIGO_ED_VALOR = 'TOD'
CODIGO_FAVORECIADO = '&codigoFavorecido='
SEARCH_URL = BASE_URL + PERIODO_INICIO + PERIODO_INICIO_VALOR + PERIODO_FIM + PERIODO_FIM_VALOR + FASE + FASE_VALOR + CODIGO_OS + CODIGO_OS_VALOR

#string de conexão do banco de dados
conn_string = "host='localhost' dbname='portaltransparencia' user='postgres' password='senha'"

#inicialização do objeto de simulação de navegador
br = Browser() 

try :
    conn = psycopg2.connect(conn_string)
except :
    print "problema ao conectar no banco de dados"

#primeira solicitação no portal da transparência
try :
	LRequest = urllib2.Request(SEARCH_URL," " )
	LResponse = br.open(LRequest)
	page = bs_parse(LResponse.read())
	print SEARCH_URL
	print page
	#f.write(page)
except :
    print "problema ao realizar primeira consulta na web"

#grava array com orgaos superiores e apresenta logs do processo na tela
print "################### Orgao Superiores ###################"
a = []
b = []

#cursor para naveção no banco de dados
cursor = conn.cursor()

#print page('form')[i]('select')[j]['id']
for i in range(len(page('form'))):
        for j in range(len(page('form')[i]('select'))):
            if page('form')[i]('select')[j]['id'] == 'avancadaOS':
                for k in range(len(page('form')[i]('select')[j]('option'))):
                    if page('form')[i]('select')[j]('option')[k]['value'] != "TOD" :
                        string = "INSERT INTO orgao_superior values(" + page('form')[i]('select')[j]('option')[k]['value'] + ",'" + page('form')[i]('select')[j]('option')[k].string + "')"
                        cursor.execute( string )
                        a.append(string)
print a
conn.commit()
