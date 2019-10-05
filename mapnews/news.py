#definiendo opciones para que sea chrome headless
import time, re, datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import spacy.cli

spacy.cli.download("es_core_news_sm")
nlp_es = spacy.load('es_core_news_sm')
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
fecha_requerida = '2019,10,1'
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

  prevfecha= re.findall(r"sociedad/[0-9]{4}/[0-9]*/[0-9]*",url1)
  fecha = prevfecha[0] if prevfecha else 'sociedad/2019/01/01'
  fecha = fecha[9:].replace('/', '-')

  tagind = sopita.find('meta', attrs={"name": 'keywords'})
  tags = tagind.get('content')
  time.sleep(2)
  return [tags, fecha, texto_desc]

# articles = articles[0:3]

for art in articles:
  urlpart = 'http://larepublica.pe'+art[2]
  art.insert(3,text_noticia(urlpart)[0])
  art.insert(4,text_noticia(urlpart)[1])
  art.insert(5,text_noticia(urlpart)[2])

for l in articles:
  print(l[1],"-",l[4])




for art in articles:
    doc= nlp_es(art[5])
    art.insert(6,[])
    for entity in doc.ents:
        if entity.label_ == 'LOC':
            art[6].append("%s ,PER" % entity.text)

# for l in articles:
#   print(l[1],"-",l[4], "-", l[6])

articles_lug=[]

for artic in articles:
    for lug in artic[6]:
        row= artic[:6]
        # print(lug)
        row.append(lug)
        articles_lug.append(row)
print ("-------------")

# for l in articles_lug:
#     print(l[1], "-", l[4], "-", l[6])

# {"type":"Point","coordinates":[-75.761719,-11.243062]}

from arcgis.gis import GIS
from arcgis.geocoding import geocode, reverse_geocode

gis = GIS()

for lug in articles_lug:
    geocode_res = geocode( address=lug[6], as_featureset=True, max_locations=1)
    xy= geocode_res.features[0]
    gdpoint = xy.as_dict["geometry"]
    attr = xy.as_dict["attributes"]
    geom = '{"type": "Point", "coordinates": [%(x)s, %(y)s]}'
    geomxy =geom % {'x':gdpoint["x"], 'y':gdpoint["y"]}
    lug.insert(7,geomxy)
    lug.insert(8, [attr["Match_addr"], attr["Score"]])

for l in articles_lug:
    print(l[1], "-", l[4], "-", l[6],"-",l[7],"-",l[8])


import sqlite3

conn = sqlite3.connect('../db.sqlite3')
cursor = conn.cursor()
sql = """INSERT INTO mapnews_mapnewshotspot(title,description,geom, fecha, tags, lugar) VALUES{}"""
for i in articles_lug:
    print(sql.format((i[1],i[5],i[7],i[4],i[3])))
    desc = i[5].replace('"','\"')
    cursor.execute(sql.format((i[1],desc[:1000],i[7],i[4],i[3],i[6])))
    conn.commit()
cursor.close()