import spacy.cli
import pandas as pd

from arcgis.gis import GIS
from arcgis.geocoding import geocode
from arcgis.geometry import Point


nlp_es = spacy.load('es_core_news_sm')
gis = GIS()

text = 'El Ministerio de Vivienda recibirá hoy, en la sede del sector, a los dirigentes de la comunidad shipibo-conibo de Cantagallo, en el Rímac, a fin de que ambas partes expongan claramente sus posiciones respecto al proyecto habitacional en esta zona, anunciado por la citada cartera tras el incendio ocurrido en noviembre del 2016, el cual afectó 430 viviendas y dejó en la calle a decenas de familias. ► Cantagallo: un recuento de las promesas incumplidas a la comunidad shipibo-conibo ► Cantagallo: comunidad shipibo-conibo retornó al terreno que desocuparon en el 2017 | VIDEO Durante la madrugada de ayer, más de 200 familias de la referida comunidad shipibo-conibo retornaron a Cantagallo tras denunciar que el Ministerio de Vivienda anunció la cancelación del proyecto habitacional en la zona. El plan contempla el levantamiento de 238 casas a través del programa Techo Propio. En abril de este año, el sector Vivienda informó que en octubre se iniciarían las obras Sin embargo, el ministerio nuevamente volvió a aplazar el proyecto e informó aquella vez que este comenzaría en enero de 2020. Los miembros de la comunidad shipibo-conibo manifestaron que decidieron retornar al terreno -del que son posesionarios desde el 2007- porque se sienten defraudados por el Estado. En un recorrido por este lugar, El Comercio constató que se han colocado estacas y piedras en algunos sectores, incluso, ya hay familias que han levantado carpas y toldos. César Maynas, jefe de la comunidad, dijo a este Diario que el Ministerio de Vivienda les hizo llegar un informe que señala que esta parte del terreno de Cantagallo no es apto para construir. “Después del incendio, el entonces presidente Pedro Pablo Kuczynski vino a la comunidad y prometió que iban a construir un proyecto de vivienda para la comunidad de Cantagallo. Han pasado tres años, pero hasta el momento no se ha hecho nada. El viernes pasado hemos tenido reunión con el Ministerio de Vivienda donde nos informa de que el estudio de suelo y subsuelo arroja que hay contaminación de arsénico y plomo en esta zona”, indicó. Sin embargo, Maynas afirmó que el Centro Peruano Japonés de Investigaciones Sísmicas y Mitigación de Desastres (CISMID) había realizado un estudio tras el incendio en el que precisaba que el terreno sí era apto. “Nos prometieron que cada uno iba a tener su terreno y su título de propiedad, pero hasta la fecha no han cumplido. Hemos perdido la credibilidad en el Ministerio de Vivienda”, expresó. -Reunión- Alrededor del mediodía, autoridades del sector Vivienda llegaron hasta Cantagallo para reunirse con la comunidad y escuchar sus demandas. El viceministro de Vivienda y Urbanismo, David Alfonso Ramos López, precisó que el proyecto habitacional no ha sido cancelado, sino que continúa, y que actualmente se están buscando las vías necesarias para cumplir con las promesas hechas en años anteriores por la cartera ministerial. “Retomemos el día de mañana el compromiso de que vamos a escuchar la propuesta de sus dirigentes y así seguir con el proyecto. Este no se ha cancelado, este continúa, sino que estamos viendo las alternativas viables para que ustedes logren, no solo la titulación, sino todo lo que se les ofreció, casas dignas con servicios básicos y áreas verdes”, explicó el funcionario. La congresistas Marisa Glave también llegó hasta la zona y solicitó “mayor respeto” por parte del Gobierno hacia la comunidad shipibo-conibo, ya que esta solo viene reclamando lo que no se ha cumplido hasta el momento. Asimismo, recalcó que ellos no han invadido el terreno, pues este les pertenece. Anuncios de interés Recomendado por: Anuncios de interés Recomendado por:'

def nlp_process(text):
    doc= nlp_es(text)
    datf= dict()
    datf["name"]=[]

    for entity in doc.ents:
        if entity.label_ == 'LOC':
            datf["name"].append("%s,PER"%entity.text)

    df= pd.DataFrame(datf)

    df["x"] = 0
    df["y"] = 0
    df["Match_addr"] = ""
    df["Score"] = ""

    data = df[:]
    data_empty = data.drop(data.index[:])
    return data, data_empty

def extractAddress(data, df, indice, idDf, address):
    geocode_result = geocode(address=df.iloc[indice][address], as_featureset=True, max_locations=1)
    x = geocode_result.features[0]
    gdpoint = x.as_dict["geometry"]
    attr = x.as_dict["attributes"]
    dataF = data.append(
        pd.Series([df.iloc[indice][address], gdpoint["x"], gdpoint["y"], attr["Match_addr"], attr["Score"]],
                  index=[idDf, "x", "y", "Match_addr", "Score"]), ignore_index=True)
    return dataF


def news2sqlite():
    import sqlite3
    conn = sqlite3.connect('../db.sqlite3')

    descrip = 'El Ministerio de Vivienda recibirá hoy, en la sede del sector, a los dirigentes de la comunidad shipibo-conibo de Cantagallo, en el Rímac, a fin de que ambas partes expongan claramente sus posiciones respecto al proyecto habitacional en esta zona, anunciado por la citada cartera tras el incendio ocurrido en noviembre del 2016, el cual afectó 430 viviendas y dejó en la calle a decenas de familias. ► Cantagallo: un recuento de las promesas incumplidas a la comunidad shipibo-conibo ► Cantagallo: comunidad shipibo-conibo retornó al terreno que desocuparon en el 2017 | VIDEO Durante la madrugada de ayer, más de 200 familias de la referida comunidad shipibo-conibo retornaron a Cantagallo tras denunciar que el Ministerio de Vivienda anunció la cancelación del proyecto habitacional en la zona. El plan contempla el levantamiento de 238 casas a través del programa Techo Propio. En abril de este año, el sector Vivienda informó que en octubre se iniciarían las obras Sin embargo, el ministerio nuevamente volvió a aplazar el proyecto e informó aquella vez que este comenzaría en enero de 2020. Los miembros de la comunidad shipibo-conibo manifestaron que decidieron retornar al terreno -del que son posesionarios desde el 2007- porque se sienten defraudados por el Estado. En un recorrido por este lugar, El Comercio constató que se han colocado estacas y piedras en algunos sectores, incluso, ya hay familias que han levantado carpas y toldos. César Maynas, jefe de la comunidad, dijo a este Diario que el Ministerio de Vivienda les hizo llegar un informe que señala que esta parte del terreno de Cantagallo no es apto para construir. “Después del incendio, el entonces presidente Pedro Pablo Kuczynski vino a la comunidad y prometió que iban a construir un proyecto de vivienda para la comunidad de Cantagallo. Han pasado tres años, pero hasta el momento no se ha hecho nada. El viernes pasado hemos tenido reunión con el Ministerio de Vivienda donde nos informa de que el estudio de suelo y subsuelo arroja que hay contaminación de arsénico y plomo en esta zona”, indicó. Sin embargo, Maynas afirmó que el Centro Peruano Japonés de Investigaciones Sísmicas y Mitigación de Desastres (CISMID) había realizado un estudio tras el incendio en el que precisaba que el terreno sí era apto. “Nos prometieron que cada uno iba a tener su terreno y su título de propiedad, pero hasta la fecha no han cumplido. Hemos perdido la credibilidad en el Ministerio de Vivienda”, expresó. -Reunión- Alrededor del mediodía, autoridades del sector Vivienda llegaron hasta Cantagallo para reunirse con la comunidad y escuchar sus demandas. El viceministro de Vivienda y Urbanismo, David Alfonso Ramos López, precisó que el proyecto habitacional no ha sido cancelado, sino que continúa, y que actualmente se están buscando las vías necesarias para cumplir con las promesas hechas en años anteriores por la cartera ministerial. “Retomemos el día de mañana el compromiso de que vamos a escuchar la propuesta de sus dirigentes y así seguir con el proyecto. Este no se ha cancelado, este continúa, sino que estamos viendo las alternativas viables para que ustedes logren, no solo la titulación, sino todo lo que se les ofreció, casas dignas con servicios básicos y áreas verdes”, explicó el funcionario. La congresistas Marisa Glave también llegó hasta la zona y solicitó “mayor respeto” por parte del Gobierno hacia la comunidad shipibo-conibo, ya que esta solo viene reclamando lo que no se ha cumplido hasta el momento. Asimismo, recalcó que ellos no han invadido el terreno, pues este les pertenece. Anuncios de interés Recomendado por: Anuncios de interés Recomendado por:'
    title = 'Cantagallo: comunidad y autoridades de Vivienda entablarán hoy una mesa de diálogo'
    geom = '{"type": "Point", "coordinates": [-77.10303999999996, -12.068099999999959]}'

    df = pd.DataFrame({"title": [title], "description": [descrip], "geom": geom})

    df.to_sql('mapnews_mapnewshotspot', con=conn, if_exists='append', index=False)
    conn.execute("SELECT * FROM mapnews_mapnewshotspot").fetchall()

def main():
    df, data_empty = nlp_process(text)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    data = ""
    for n in range(len(df)):
        data = extractAddress(data_empty, df, n, "name", "name")

    print(data)

if __name__ == '__main__':
    main()