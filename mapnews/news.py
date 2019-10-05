#definiendo opciones para que sea chrome headless
import time, re, datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
# import chromedriver_binary

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome('chromedriver.exe',options=options)
#funcion para checar la condicion del while y me devuelva true si existe al menos un valor mayor
#sino me devuelve false, lo que cortaria el proceso while y no haría mas clics

def check(list1, val):
    for x in list1:
        if x>= val:
            return  True
    return False


# driver = webdriver.PhantomJS()
#ingresamos la url, con categoria
url = "https://larepublica.pe/sociedad/"
fecha_requerida = '2019,10,3'
fecha_requerida = datetime.datetime.strptime(fecha_requerida,'%Y,%m,%d')

fecha_news = datetime.datetime.now()

driver.get(url)
# html = driver.page_source.encode('cp1252')
page_num = 0
#class = btn btn-lg
#id = btnLoadMore
#div class box-load-more text-center
# while driver.find_elements_by_css_selector('#btnLoadMore'):

condicion= fecha_requerida <= fecha_news

while condicion:
    try:
      element = driver.find_element_by_id('btnLoadMore')
      driver.execute_script("arguments[0].click();", element)
      # driver.find_element_by_css_selector('#btnLoadMore').click()

      page_num += 1
      print("obteniendo la página número"+str(page_num))
      time.sleep(1)

      htmltemp = driver.page_source.encode('cp1252')
      htmltext = str(BeautifulSoup(htmltemp, 'html.parser'))
      y= re.findall(r"sociedad/[0-9]{4}/[0-9]*/[0-9]*",htmltext)
      #word.replace('/',','),
      # y= [datetime.datetime.strptime(word[9:],'%Y/%m/%d') for word in y]
      y= [word[9:].replace('/','-') for word in y]
      y.sort()
      sub = y[0:10]
      print(sub)

      condicion = check(sub,fecha_requerida)

    except Exception as e:
      print(e)
      break
# page_num
html = driver.page_source.encode('cp1252')
print(html)


from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
# links = soup.find_all('div', attrs={"class":'search-result-indiv'})
# links = soup.find_all('h3', attrs={"class":'c01386'})
links = soup.find_all('ul', attrs={"class":'c01383'})


articles = [[a.find("span").get_text(),a.find('a').get_text(),a.find('a')['href']] for a in links if a != '']
articles.sort(key =lambda x: x[2])
len(articles)
# print(articles)


import datetime
d1 = datetime.datetime(2018,9,22)
d2 = datetime.datetime(2018,5,3)
l= [d1,d2]



def text_noticia(url1):
  url_prueba = url1
  resultado = requests.get(url_prueba)
  contenido = resultado.content
  sopita = BeautifulSoup(contenido, 'html.parser')
  bodytext = sopita.find('div', attrs={"class":'page-internal-content'})
  parrafos = bodytext.find_all('p')
  parrafos = [p.get_text() for p in parrafos if 'PUEDES VER'not in p.get_text()]
  texto_desc= '\n'.join(parrafos)

  fecha = re.findall(r"sociedad/[0-9]{4}/[0-9]*/[0-9]*",url1)[0]
  fecha = fecha[9:].replace('/', '-')

  tagind = sopita.find('meta', attrs={"name": 'keywords'})
  tags = tagind.get('content')
  time.sleep(2)
  return [tags, fecha, texto_desc]

listprueb = articles[0:3]

for art in listprueb:
  urlpart = 'http://larepublica.pe'+art[2]
  art.insert(3,text_noticia(urlpart)[0])
  art.insert(4,text_noticia(urlpart)[1])
  art.insert(5,text_noticia(urlpart)[2])

for l in listprueb:
  print(l[1],"-",l[4])

