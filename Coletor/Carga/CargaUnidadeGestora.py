'''
Created on 16/06/2013

@author: raulc_000

Script que captura todos oas Unidades Gestoras do Governo presentes no Portal da Transparência e as vincula a um Orgão determinado
'''
#importa bibliotecas
import urllib ,urllib2
import time
import psycopg2
from BeautifulSoup import BeautifulSoup as bs_parse
from mechanize import Browser
import re

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

br.close()

#grava array com orgaos superiores e apresenta logs do processo na tela
print "################### Unidade Gestora ###################"
a = []
b = []

#cursor para naveção no banco de dados
cursor = conn.cursor()

#consulta orgão para vincular a unidades gestoras
stringSQL = "select org.codigo_os, org.codigo, ug.codigo_orgao from orgaos as org left join unidade_gestora as ug on org.codigo = ug.codigo_orgao where ug.codigo_orgao is NULL;"

#cursor.execute("Select a.codigo, b.codigo from orgao_superior as a, orgaos as b where a.codigo = b.codigo_os;")

cursor.execute(stringSQL)

rows = cursor.fetchall()

for row in rows:
    br = Browser() 
    SEARCH_URL = BASE_URL + PERIODO_INICIO + PERIODO_INICIO_VALOR + PERIODO_FIM + PERIODO_FIM_VALOR + FASE + FASE_VALOR + CODIGO_OS + str(row[0]) + CODIGO_ORGAO + str(row[1])
    print SEARCH_URL
    LRequest = urllib2.Request(SEARCH_URL," " )
    LResponse = br.open(LRequest)
    page = bs_parse(LResponse.read())
    time.sleep(3)
    for i in range(len(page('form'))):
        for j in range(len(page('form')[i]('select'))):
            if page('form')[i]('select')[j]['id'] == 'listaUGs':
                for k in range(len(page('form')[i]('select')[j]('option'))):
                    if page('form')[i]('select')[j]('option')[k]['value'] != 'TOD' and page('form')[i]('select')[j]('option')[k].string != 'Todos' :
                        string = page('form')[i]('select')[j]('option')[k].string
                        string = re.sub('[\'!@#$;]', ' ', string)
                        string = "INSERT INTO unidade_gestora values(" + str(row[0]) + ',' + str(row[1]) + ',' + page('form')[i]('select')[j]('option')[k]['value'] + ",'" + string + "');"
                        cursor.execute( string )
                        print string

    br.close()
    conn.commit()        

#print rows
