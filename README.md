# *Trust* UnB - *Social Engineering*  

Este projeto consiste em um *scrapper* que retira dados do portal de [transparência do governo federal](http://www.portaltransparencia.gov.br/) referentes a licitações, e os organiza em um banco de dados *Postgree* com a finalidade de identificar os papeis de corretagem dos agentes envolvidos.

## Como utilizar
O projeto é dividido em dois grandes módulos o **Coletor** e o **Montador**. O coletor faz o *scrapping* do portal de transparência, enquanto o montador modela os dados no formato que a feramenta *Pajek* possa transformá-los em uma rede para facilitar a análise destes.

### Pré requisitos
* Python
* Banco de dados *Postgree*
* Biblioteca *beautiful soup*
* Biblioteca *mechanize*
* Biblioteca *stem*
* Biblioteca *psycopg2*
* Outras bibliotecas padrão do *python*

### *Ubuntu*
Para utilizar o projeto no *Ubuntu* primeiro devemos ter o *Postgree* instalado. Para instalar rode no terminal os comandos:

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

faça o backup do banco de dados utilizando o arquivo presente na pasta '/data/banco'

## Equipe
* [**Raul Carvalho de Souza**](https://github.com/raulcsouza) - Trabalho inicial (pesquisa e código fonte)
* [**Jefferson Viana Fonseca Abreu**](https://github.com/jeffvfa) - Aprimoramento do sistem
