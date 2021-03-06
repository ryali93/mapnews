import sqlite3
# import pandas as pd
# conn = sqlite3.connect('../db.sqlite3')

# a = pd.read_sql('select * from mapnews_mapnewshotspot', conn)
# print(a)

# descrip = 'El Ministerio de Vivienda recibirá hoy, en la sede del sector, a los dirigentes de la comunidad shipibo-conibo de Cantagallo, en el Rímac, a fin de que ambas partes expongan claramente sus posiciones respecto al proyecto habitacional en esta zona, anunciado por la citada cartera tras el incendio ocurrido en noviembre del 2016, el cual afectó 430 viviendas y dejó en la calle a decenas de familias. ► Cantagallo: un recuento de las promesas incumplidas a la comunidad shipibo-conibo ► Cantagallo: comunidad shipibo-conibo retornó al terreno que desocuparon en el 2017 | VIDEO Durante la madrugada de ayer, más de 200 familias de la referida comunidad shipibo-conibo retornaron a Cantagallo tras denunciar que el Ministerio de Vivienda anunció la cancelación del proyecto habitacional en la zona. El plan contempla el levantamiento de 238 casas a través del programa Techo Propio. En abril de este año, el sector Vivienda informó que en octubre se iniciarían las obras Sin embargo, el ministerio nuevamente volvió a aplazar el proyecto e informó aquella vez que este comenzaría en enero de 2020. Los miembros de la comunidad shipibo-conibo manifestaron que decidieron retornar al terreno -del que son posesionarios desde el 2007- porque se sienten defraudados por el Estado. En un recorrido por este lugar, El Comercio constató que se han colocado estacas y piedras en algunos sectores, incluso, ya hay familias que han levantado carpas y toldos. César Maynas, jefe de la comunidad, dijo a este Diario que el Ministerio de Vivienda les hizo llegar un informe que señala que esta parte del terreno de Cantagallo no es apto para construir. “Después del incendio, el entonces presidente Pedro Pablo Kuczynski vino a la comunidad y prometió que iban a construir un proyecto de vivienda para la comunidad de Cantagallo. Han pasado tres años, pero hasta el momento no se ha hecho nada. El viernes pasado hemos tenido reunión con el Ministerio de Vivienda donde nos informa de que el estudio de suelo y subsuelo arroja que hay contaminación de arsénico y plomo en esta zona”, indicó. Sin embargo, Maynas afirmó que el Centro Peruano Japonés de Investigaciones Sísmicas y Mitigación de Desastres (CISMID) había realizado un estudio tras el incendio en el que precisaba que el terreno sí era apto. “Nos prometieron que cada uno iba a tener su terreno y su título de propiedad, pero hasta la fecha no han cumplido. Hemos perdido la credibilidad en el Ministerio de Vivienda”, expresó. -Reunión- Alrededor del mediodía, autoridades del sector Vivienda llegaron hasta Cantagallo para reunirse con la comunidad y escuchar sus demandas. El viceministro de Vivienda y Urbanismo, David Alfonso Ramos López, precisó que el proyecto habitacional no ha sido cancelado, sino que continúa, y que actualmente se están buscando las vías necesarias para cumplir con las promesas hechas en años anteriores por la cartera ministerial. “Retomemos el día de mañana el compromiso de que vamos a escuchar la propuesta de sus dirigentes y así seguir con el proyecto. Este no se ha cancelado, este continúa, sino que estamos viendo las alternativas viables para que ustedes logren, no solo la titulación, sino todo lo que se les ofreció, casas dignas con servicios básicos y áreas verdes”, explicó el funcionario. La congresistas Marisa Glave también llegó hasta la zona y solicitó “mayor respeto” por parte del Gobierno hacia la comunidad shipibo-conibo, ya que esta solo viene reclamando lo que no se ha cumplido hasta el momento. Asimismo, recalcó que ellos no han invadido el terreno, pues este les pertenece. Anuncios de interés Recomendado por: Anuncios de interés Recomendado por:'
# title = 'Cantagallo: comunidad y autoridades de Vivienda entablarán hoy una mesa de diálogo'
# geom = '{"type": "Point", "coordinates": [-77.10303999999996, -12.068099999999959]}'
# df = pd.DataFrame({"title": [title], "description": [descrip], "geom": geom})
#
# df.to_sql('mapnews_mapnewshotspot', con=conn, if_exists='append', index=False)
# conn.execute("SELECT * FROM mapnews_mapnewshotspot").fetchall()
#
# a = pd.read_sql('select * from mapnews_mapnewshotspot', conn)
# print(a)

# cursor = conn.cursor()
#
# cursor.execute('select * from mapnews_mapnewshotspot')
# for u in cursor:
#     print(u)
#
# x=cursor.execute( 'pragma table_info(mapnews_mapnewshotspot)')
#
# colnames = x.description
# for row in x:
#     print(row)
# #
# sql = 'INSERT INTO mapnews_mapnewshotspot(title,description,geom, fecha, tags) VALUES{}'
# for i in articles:
#     cursor.execute(sql.format((i[1],str(i[5]),i[7],i[4],i[3])))
#     cursor.commit()
# cursor.close()

conn = sqlite3.connect('../db.sqlite3')
cursor = conn.cursor()
sql= 'DELETE FROM mapnews_mapnewshotspot WHERE dia IS NULL'
cursor.execute(sql)
conn.commit()