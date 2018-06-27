from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import urllib.parse
import math
import sys
from datetime import datetime
import os
import re
import sqlite3
import string
import unicodedata
import urllib
from operator import itemgetter
from random import randrange
from socket import *
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from PyPDF2 import PdfFileReader
import PyPDF2 as pyPdf
import matplotlib.pyplot as plt
import requests
import requests.exceptions as rex
from bs4 import BeautifulSoup
import time
import subprocess


def rm():
    path = "/tmp/"
    dir = os.listdir(path)
    for file in dir:
        if file == "pdffile.pdf":
            try:
                os.remove(file)
            except Exception as e:
                return e
    return True
def stopWords(path='/home/roger/Documents/Pesquisa/portuguese_stopwords'):
    arq =(open(path,'r').read()).split("\n")
    return arq
def goffmanPoint(rept):
    return round(((-1 + math.sqrt(1 + 8 * rept)) / 2), 0)
def RemoveAccents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).upper()
def wordcloud(text, path):
    listofwords = []
    with open("/home/pesquisa/Downloads/stopwords.txt") as file:
        for line in file:
            listofwords.append(line)
    stopwords = set(listofwords)
    wordcloud = WordCloud(background_color="white", stopwords=stopwords, max_font_size=100, width=1520, height=535,
                          relative_scaling=0.5, max_words=4000).generate(text)
    plt.figure(figsize=(16, 9))
    plt.imshow(wordcloud)
    plt.axis("off")
    try:
        plt.savefig(path + GetRandomName() + ".png", dpi=100)
    except:
        print("error generating wordcloud")
        return None
def get_text_from_pdf(url):
    pages = ""
    path = "/home/roger/Documents/Pesquisa/pdfs/file.pdf"
    try:
        r = requests.get(url, allow_redirects=True)
    except requests.exceptions.ConnectionError:
        return False
    open(path, 'wb').write(r.content)
    pdf_file = open(path, 'rb')
    read_pdf = pyPdf.PdfFileReader(pdf_file)
    if read_pdf.isEncrypted:
        try:
            read_pdf.decrypt('')
        except NotImplementedError:
            return log_file(url)
    number_of_pages = read_pdf.getNumPages()
    for pageNum in range(number_of_pages):
        page = read_pdf.getPage(pageNum)
        page_content = page.extractText()
        pages += page_content
    if len(pages)<60:
        return log_file(url)
    else:
        return date_of_links((pages,url),2)


    return date_of_links((text,url),2)
def CounterWords(text, url):
    listofwords = stopWords()
    eixos = []
    frequency = {}
    words = re.findall(r"(\b[A-Za-z][a-z]{4,40}\b)", text.lower())
    for word in words:
        count = frequency.get(word, 0)
        frequency[word] = count + 1
    for key, value in reversed(sorted(frequency.items(), key=itemgetter(1))):
        if  not key in listofwords:
            eixos.append([key, value])
    return eixos
    # l_sorted = sorted(eixos, key=lambda x: x[1], reverse=True)
    rank = 1
    # try:
    #     l_sorted[0].append(rank)
    # except IndexError:
    #     return ErroReport(url)
    # for i in range(len(l_sorted) - 1):
    #     if (l_sorted[i][1] != l_sorted[i + 1][1]):
    #         rank += 1
    #     try:
    #         l_sorted[i + 1].append(rank)
    #     except IndexError:
    #         return ErroReport(url)


    # return l_sorted
        # InsertDate(l_sorted, url)



    # else:
    #     ErroReport(url)
    #     return "There were errors in the process \n check the bug report: /tmp/ReportOfErrors.txt"
def DotheGraph(lista, path, url):
    repet = []
    posi = []
    zipf = []
    for i in lista:
        repet.append(i[1])
        posi.append(i[2])

    maximo = max(repet)
    for i in lista:
        zipf.append(maximo / i[2])

    plt.figure()
    plt.rcParams.update({'figure.max_open_warning': 0})
    ax1 = plt.subplot(2, 1, 1)
    plt.ylabel("Distrib. zipf")
    ax1.plot(posi, zipf, 'o-')

    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(posi, repet, '.-')
    plt.xlabel("Ranking")
    plt.ylabel("Repetições")
    try:
        plt.savefig(path + GetRandomName() + ".png", dpi=100)
    except:
        print("erro ao gerar grafico..")
        return 0
    plt.clf()
    plt.close('all')
def log_file(url):
    print("writing log file...")
    path = "/home/roger/Documents/Pesquisa/logfile_{}".format(datetime.now().ctime())
    file = open(path,'w')
    file.write("The url:{} have a small or non-existent string.".format(url))
    file.close()
    return "log file saved"
def testeLink(url):
    headers_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        response = requests.get(url,timeout=None,headers=headers_agent )
        print("estatus da requisição: {}".format(response.status_code))
        return response.status_code
    except Exception as e:
        print("erro ao conectar a URL: {}".format(e))
        return False
def get_text_from_url(url):
    headers_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        request=urlopen(Request(url, headers=headers_agent))
    except Exception as e:
        return e
    soup = BeautifulSoup(((request.read()),"html.parser")
    text = "".join([p.text for p in soup.find_all("p")])

    if text is None or len(text)<30 :
        return log_file(url)
    else:
        return date_of_links((text,url),2)
def returno_date(name,table=None,path="/home/roger/Documents/Pesquisa/"):
    if table is None:
        return "no tables entry"
    conn = sqlite3.connect(path+name)
    c = conn.cursor()
    c.execute("""SELECT * FROM """+table+""";""")
    itens= []
    for linha in c.fetchall():
        itens.append(linha)
    return itens
def create_bank(name,path="/home/roger/Documents/Pesquisa/"):
    return sqlite3.connect(path+name)
def date_of_links(dados,table=None):
    c = create_bank("date_of_links.db")
    if table==1:
        conn= c.cursor()
        try:
            conn.execute("""CREATE TABLE IF NOT EXISTS date_of_links (googlelinks text);""")
            c.commit()
        except Exception as e:
            return e
        try:
            conn.execute("""INSERT INTO date_of_links (googlelinks) VALUES(?)""",[dados])
            c.commit()
        except Exception as e:
            return e
        c.close()
        return "values successfully inserted in table"
    elif table==2:
        conn= c.cursor()
        try:
            conn.execute("""CREATE TABLE IF NOT EXISTS info_url (txt text,url text);""")
            c.commit()
        except Exception as e:
            return e
        try:
            conn.execute("""INSERT INTO info_url (txt,url) VALUES(?,?)""",(dados[0],dados[1]))
            c.commit()
        except Exception as e:
            return e
        c.close()
        return "values successfully inserted in table "
    else:
        return "chose your data tables"
def google_screper_results(termo_pesq,len):
    links_check=[]
    i=0
    headers_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    while True:
        google_url = 'https://www.google.com/search?q={}&&num={}&&hl={}&&start={}&'.format(termo_pesq, 100, len, i)
        try:
            response = requests.get(google_url,timeout=None,headers=headers_agent )
        except Exception as erro:
            print(erro)
            break
        soup=BeautifulSoup(response.content,"html.parser")
        for link in  soup.findAll('a', attrs={'href': re.compile("^http://")}):
            j =link.get('href')
            if testeLink(j)==200 and j not in links_check and not "webcache" in j:
                print(date_of_links(j,1))
                links_check.append(j)

        print("Pagina de resultados numero: {}".format(i/10))
        i+=10
        time.sleep(300)

    return "ok"
def checklist(word,list_):
    if word in list_:
        return True
    else:
        False
# print(google_screper_results("deficiencia+visual+mercado+de+trabalho+acessibilidade+inserção","pt"))
for url in returno_date('date_of_links.db','date_of_links')[41:]:
    if checklist('pdf', url[0]) or checklist('file',url[0]):
        pass
    #     print("detected pdf file format : {}".format(url[0]))
    #     get_text_from_pdf(url[0])
    #     print("wait for 200 seconds...")
    #     for i in range(100):
    #         time.sleep(1)
    #         sys.stdout.write("\r%d%%" % i)
    #         sys.stdout.flush()
    elif checklist('docx',url[0]):
        pass
    #     log_file(url[0])
    else:
        print(url[0])
        print(get_text_from_url(url[0]))
        print("wait for 4 minutes...")
        for i in range(600):
            time.sleep(1)
            sys.stdout.write("\r%d%%" % i)
            sys.stdout.flush()
