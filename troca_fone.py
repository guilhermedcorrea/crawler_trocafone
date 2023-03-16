from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
from typing import Literal, List, Generator,Any
from itertools import chain, zip_longest
from urllib import parse
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd



options = webdriver.ChromeOptions() 
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options,
                               executable_path=r"C:\estimadoresteste\crawler_trocafone\chromedriver\chromedriver.exe")


def scroll_page() -> None:
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True


def get_sub_categorias() -> Generator[str, None, None]:
    driver.implicitly_wait(7)
    driver.get("https://www.trocafone.com.br/")

    time.sleep(1)

    sub_categorias = driver.find_elements(By.XPATH
                                          ,'/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/section/div/div[2]/div/div/nav/ul/li/div/a')
    
    s_categorias = [sub.get_attribute("href") for sub in sub_categorias if sub !='']
    cont = len(s_categorias)
    i = 0
    while i < cont:
        try:
            if len(s_categorias[i]) > 3:
                yield s_categorias[i]
            i +=1
        except Exception as e:
            print(e)

def extract_item(*args, **kwargs) -> Any:
    lista_dict_produtos = []
    driver.implicitly_wait(7)
    for lista in args:
        driver.get(lista)
        time.sleep(1)
        dict_produtos = {}

        
        try:
            dict_produtos['PaginaProduto'] = lista
            nome_produto = driver.find_elements(
                By.XPATH,
                '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div[2]/section/div/div[1]/div/div/div[1]/div/div[2]/div/div[1]/div/div/div/h1/span')[0].text
        
            dict_produtos['NomeProduto'] = nome_produto
        except Exception as e:
            print(e)

        try:
            precos = driver.find_elements(By.XPATH,'/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div')
            preco = [preco.text.replace("R$","").replace(".","").replace(",",".").strip().split("\n") for preco in precos]
            prices = chain(preco)
            for pric in prices:
                dict_produtos['MenorPreco'] = min(pric)
                dict_produtos['MaiorPreco'] = pric[0]
        except Exception as e:
            print(e)


        try:
            condicoes = driver.find_elements(By.XPATH,
                                            '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div[2]/section/div/div[1]/div/div/div[1]/div/div[2]/div/div[8]/div')
        
            condices_p = [condicao.text.replace("R$","").replace(".","").replace(",",".").split("\n") for condicao in condicoes]
        
            conds = dict(zip(*[iter(*condices_p)]*2))
            dict_produtos.update(conds)
        except Exception as e:
            print(e)

        try:
            cor_produto = driver.find_elements(
                By.XPATH,'/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div[2]/section/div/div[1]/div/div/div[1]/div/div[2]/div/div[4]/div/div[1]/div/div[1]/span[3]')[0].text
        
            dict_produtos['CorProduto'] = cor_produto

            armazenamento_produto = driver.find_elements(By.XPATH,'/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div[2]/section/div/div[1]/div/div/div[1]/div/div[2]/div/div[5]/div[2]/button[1]')[0].text
        
            dict_produtos['Armazenament'] = armazenamento_produto
        except Exception as e:
            print(e)

        try:
            imagens = driver.find_elements(By.XPATH
                                        ,'/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div[2]/section/div/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div/div/div/div/img')
            cont = 0
            for imagem in imagens:
                dict_produtos['imagem'+str(cont)] = imagem.get_attribute("srcset")
                cont +=1
        except Exception as e:
            print(e)

        print(dict_produtos)
        lista_dict_produtos.append(dict_produtos)
    
    
    return lista_dict_produtos


def get_url_produtos() -> list:
    lista_produtos = []
    driver.implicitly_wait(7)
    categorias = get_sub_categorias()
    try:
        for categoria in categorias:
            driver.get(categoria)
            scroll_page()
           
            produtos_url = driver.find_elements(By.XPATH,'//*[@id="gallery-layout-container"]/div/section/a')
            p_urls = [urls.get_attribute("href") for urls in produtos_url]
            new_dicts = extract_item(*p_urls)
            lista_produtos.append(new_dicts)

            
    except Exception as e:
        print(e)
    
    return lista_produtos


produtos = get_url_produtos()

data = pd.DataFrame()
data.to_excel("lista_produtos_trocafone.xlsx")
