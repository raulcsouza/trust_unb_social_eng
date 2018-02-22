#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 05/03/2014

@author: raulc_000

Cria rede no formato .net para o sistema PAJEK e grupos, classificações, clusters.
'''
import psycopg2
import sys
from ConsultasAvancadas import gravalog

f = None

def gravaArquivo(f, texto):
    try :
        f.write(texto + "\n")
        f.flush()
    except :
        print "Problemas ao gravar no arquivo"
        sys.exit()

arquivo = '../../data/rede_pajek.net'
f = open(arquivo,'w')

conn_string = "host='193.169.1.8' dbname='portaltransparencia' user='postgres' password=senha'"

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

stringSQL = "select DISTINCT(ug.codigo), ug.descricao    from unidade_gestora as ug, consulta as con"
stringSQL =  stringSQL +  " where ug.codigo = con.unidade_gestora and data_inicio like '%2014%' order by ug.codigo;"

cursor.execute(stringSQL)

rows = cursor.fetchall()

dict = {}

count = 1
for row in rows:
    aux = row[1]
    dict[aux] = count
    count = count + 1

aux2 = len(dict)

stringSQL = "select DISTINCT(TRIM(regexp_replace(favorecido, E'[\\n\\r\\u2028\\t]+' || '[[:space:]]*[[:space:]]', '', 'g'))) as favorecido from consulta where data_inicio like '%2014%' and favorecido not like '%R$%';"

cursor.execute(stringSQL)

rows = cursor.fetchall()

for row in rows:
    aux =  row[0]
    dict[aux] = count
    count = count + 1


d = sorted(dict, key=lambda x : dict[x])

print "*Vertices " + str(len(d)) + " "  + str(aux2)
gravaArquivo(f,"*Vertices " + str(len(d)) + " "  + str(aux2))

for x in d:
    print "%s \"%s\"" % (dict[x], x)
    gravaArquivo(f,"%s \"%s\"" % (dict[x], x))

#print dict[' 24.073.694/0001-55 - C I L COMERCIO DE INFORMATICA LTDA ']
print "*Edges"
gravaArquivo(f,"*Edges")

stringSQL = "select ug.descricao, TRIM(regexp_replace(con.favorecido, E'[\\n\\r\\u2028\\t]+' || '[[:space:]]*[[:space:]]', '', 'g')) from unidade_gestora as ug, consulta as con "
stringSQL =  stringSQL + "where ug.codigo = con.unidade_gestora and data_inicio like '%2014%' and favorecido not like '%R$%' order by ug.codigo;"

cursor.execute(stringSQL)

rows = cursor.fetchall()

for row in rows:
    print str(dict[row[0]]) + " " + str(dict[row[1]])
    gravaArquivo(f,str(dict[row[0]]) + " " + str(dict[row[1]]))

arquivo2 = '//home//raul//Documents//unb_python//data//rede_pajek_partition.clu'
f2 = open(arquivo2,'w')

print "*Vertices " + str(len(d))
gravaArquivo(f2,"*Vertices " + str(len(d)))

for x in d:
    if int(dict[x]) <= int(aux2):
        print "1"
        gravaArquivo(f2, "1")
    else :
        print "2"
        gravaArquivo(f2, "2")
