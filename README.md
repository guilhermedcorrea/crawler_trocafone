##Execução do projeto
<br>criar venv: py -3 -m venv venv<br/>
<br>ativar: venv\Scripts\activate<br/>
<br>instalar dependencias: pip freeze > requirements.txt<br/>



```Python

options = webdriver.ChromeOptions() 
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options,
                               executable_path=r"C:\estimadoresteste\crawler_trocafone\chromedriver\chromedriver.exe")
...

<br>Informar caminho doo arquivo chromedriver referente a versao quee sta utilizando <br/>

``` Python
def get_sub_categorias() -> Generator[str, None, None]:
    driver.implicitly_wait(7)
    driver.get("https://www.trocafone.com.br/")

    time.sleep(1)

    sub_categorias = driver.find_elements(By.XPATH
                                          ,'/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/section/div/div[2]/div/div/nav/ul/li/div/a')
    
    s_categorias = [sub.get_attribute("href") for sub in sub_categorias if sub !='']

```

<br> Itera na home extraindo as urls dos departamentos usando o xpath<br/>



``` Python

def get_url_produtos() -> list:
    lista_produtos = []
    driver.implicitly_wait(7)
    categorias = get_sub_categorias()

```

<br>Recebe o retorno da função  get_sub_categorias() Itera por ela e faz o driver.get usand o scroll_page para rolar a pagina e o xpath extrair a url dos produtos<br/>



``` Python

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

```

<br>Função extract_item Recebe como paramentro a url do produto faz o driver.get extrai as informações da pagina usand o xpath,armazena em um dicionario e faz o append em uma lista, ao final a função retorna a lista de dicionaris que é salva em um dataframe e apartir dele gerado um arquivo .xlsx<br/>