# Recomendación de Películas
## Proyecto 1: Machine Learning Operations (MLOps)

![Peliculas](images/peli.PNG)
### Objetivo del proyecto
Dados dos dataset con información de películas: titulo, fecha de estreno, facturación , casting , etc. Lo que se busca es lograr transformaciones y exploraciones que permitan luego generar un sistema de recomendación fiable.La idea es que, consultada una película, nos devuelva películas similares para recomendar.


![Cloud](images/wordcloud.png)
### [MVP](#mvp)
Para este MVP se generaron algunas transformaciones en Python: 
-	Columnas : belongs_to_collection, production_companies fueron desanidadas ya que no permitían acceder a la información y tenían datos en formatos que no se necesitaban.
- Los valores nulos de los campos revenue, budget fueron rellenados por el número 0.
-	Los valores nulos del campo release date se eliminaron.
-	En las columnas donde había fechas, se pasó a formato AAAA-mm-dd, y se creó la columna release_year de donde se extrae el año de la fecha de estreno.
-	Se creo la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas revenue / Budget. Cuando no se encontraron datos disponibles para calcularlo, se llenó con el valor 0.
-	Se eliminaron las columnas: adult , video, imdb_id, adult, original_title, poster_pathy homepage.
Otras transformaciones: 
- Se crearon columnas con días y meses en castellano para luego generar funciones para la consultas de la api 
-	Además para poder acceder a otras consultas : se desanido el dataset de créditos en las columnas de director y actor .
-	Se crearon datasets solo con las columnas que eran necesarias para las funciones y así se podria acceder a la informacion de manera mas efectiva. [Data]( https://github.com/mariangigena/Recomendacion-peliculas-P1/tree/main/data)
### [Api](#api)
Se utilizo el framework FastAPI .
Se crearon  6 funciones para los endpoints que se consumirán en la API
- def cantidad_filmaciones_mes( Mes) : Se ingresa un mes en idioma Español. Devuelve la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del conjunto de datos.
-	def cantidad_filmaciones_dia( Dia) : Se ingresa un día en idioma Español. Devuelve la cantidad de películas que fueron estrenadas en el día consultado en la totalidad del conjunto de datos.
- def score_titulo( titulo_de_la_filmación) : Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
- def votos_titulo( titulo_de_la_filmación) : Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. Tiene que contar con al menos 2000 valoraciones, caso contrario, devuelve un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.
- def get_actor( nombre_actor) : Se ingresa el nombre de un actor que se encuentra dentro de un dataset .Devuelve el éxito del mismo medido a través del retorno. Además, la cantidad de películas que ha realizado y el promedio de retorno. 
- def get_director( nombre_director) : Se ingresa el nombre de un director . Devuelve el éxito del mismo medido a través del retorno. Además el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.


Deployment: se utilizo Render para poder generar el deploy. https://recomendacion-peliculas-wxvx.onrender.com/


### [Modelo de recomendacion](#modelo-de-recomendacion) 
El código que está en el archivo :[modelo]( https://github.com/mariangigena/Recomendacion-peliculas-P1/blob/main/code/modelo.ipynb) carga un dataset de películas desde un archivo CSV llamado ‘movies.csv’, selecciona algunas columnas de interés y las guarda en un nuevo archivo CSV llamado ‘moviesml.csv’. 
Luego, el código realiza algunos cálculos para determinar el promedio de votos y el número mínimo de votos requeridos para ser incluido en la lista de películas calificadas. Después, se filtran las películas que cumplen con estos criterios y se calcula una puntuación ponderada para cada película utilizando la fórmula de promedio ponderado de Bayes.
A continuación, el código utiliza la clase TfidfVectorizer de scikit-learn para calcular la matriz TF-IDF de las descripciones de las películas. 
Esta matriz se utiliza para calcular la similitud del coseno entre las películas, que es una medida comúnmente utilizada en sistemas de recomendación para calcular la similitud entre elementos. La elección se basó en la simpleza que conlleva y en la facilidad que permite para los procesos posteriores (deploy). Luego, se crea un diccionario que mapea los títulos de las películas a sus índices en la matriz de similitud del coseno.
Finalmente, el código define una función llamada recomendación que toma como entrada un título de película y devuelve una lista de las 5 películas más similares a la película ingresada utilizando la similitud del coseno para calcular la similitud entre las películas. Esta función convierte el título ingresado a minúsculas y utiliza un diccionario con los títulos en minúsculas para buscar el índice de la película en la matriz de similitud del coseno. Por ultinmo, se obtienen los puntajes de similitud para todas las películas con respecto a la película ingresada, se ordenan en orden descendente y se seleccionan las 5 películas más similares.

### Documentacion
-	[Scikit-learn]( https://scikit-learn.org/stable/index.html#)
-	[FastAPI](https://fastapi.tiangolo.com/es/)
-	[Render](https://render.com/docs)
-	[Pandas](https://pandas.pydata.org/docs/)

### Contacto
[linkedin](https://www.linkedin.com/in/mariana-gigena/)



