
from pandas.io.formats.format import IntArrayFormatter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.select import Select
import time
from webdriver_manager.chrome import ChromeDriverManager
import pyodbc
import operator
import json
import re

driver = webdriver.Chrome(ChromeDriverManager().install())

def tratar_infos(elementos):
        valor = elementos.replace("vtex.events.addData(","").replace(");","")
        return valor


def separa_infos(elementos):
    desc_infos = {}
  
    if re.search('^Tecnologias de Destaque:|-\.?\w.*\s+\$',elementos,re.I):
        desc_infos['Tecnologias de Destaque'] = elementos
        
    elif re.search('^Dados técnicos:|-\.?\w.*\s+\$',elementos,re.I):
        try:
            desc_infos['Dados técnicos'] = elementos
        except:
            desc_infos['Dados técnicos'] = "NotFound"

    elif re.search('^Recursos adicionais:|-\.?\w.*\s+\$',elementos,re.I):
        try:
            desc_infos['Recursos adicionais'] = elementos
        except:
            desc_infos['Recursos adicionais'] = "NotFound"
   
    elif re.search('^O que contém a embalagem:|-\.?\w.*\s+\$',elementos,re.I):
        try:
            desc_infos['O que contém a embalagem'] = elementos
        except:
            desc_infos['O que contém a embalagem'] = "NotFound"

    else:

        try:
            desc_infos["Descrição"] = elementos
        except:
            desc_infos["Descrição"] = "NotFound"

    return desc_infos


items = []


df_urls = pd.read_excel('links_dlink.xlsx')
for i, row in df_urls.iterrows():
    driver.get(row[0])

    desc = {}
    cont = 1
    try:
        imagem = driver.find_elements_by_xpath("//ul[@class='thumbs']/li/a//img")
        for img in imagem:
            imgs = img.get_attribute("src").replace('100-100','1000-1000')
            desc["imagem"+str(cont)] = imgs
            cont+=1
    except:
        Error="NotFound"
        
    try:
        json_infos = driver.find_elements_by_xpath("//*[contains(text(), 'vtex.events.addData')]")
        for x in json_infos:
            jsons = tratar_infos(x.get_attribute("textContent"))
            valores = json.loads(jsons)
            desc.update(valores)
            items.append(desc)
    except:
        items.append("NotFound")
        
    time.sleep(1)

    infos_tecnicas = driver.find_elements_by_xpath("//div[@class='productDescription']//p")
    for infos in infos_tecnicas:
        infos_teste = separa_infos(infos.text)

    desc.update(infos_teste)

    items.append(desc)

    print(desc)

try:
    df_infos = pd.DataFrame(items)
    df_infos.to_excel("testedlink.xlsx")
except:
    print("NotFound")



