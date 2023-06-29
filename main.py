from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = FastAPI()

class Pelicula(BaseModel):
    titulo: str
    anio: str
    retorno_pelicula: float
    budget_pelicula: float
    revenue_pelicula: float

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia):
    data = pd.read_csv('data\nuevo_data.csv')
    dia_consultado = dia.capitalize()
    filmaciones_dia = data[data['nombre_dia'] == dia_consultado]
    return f"La cantidad de peliculas estrenadas en el dia {dia_consultado} es: {len(filmaciones_dia)}"

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes):
    data = pd.read_csv('data\nuevo_data.csv.csv')
    mes_consultado = mes.lower()
    filmaciones_mes = data[data['nombre_mes'] == mes_consultado]
    return f"La cantidad de peliculas estrenadas en el mes de {mes_consultado} es: {len(filmaciones_mes)}"

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo):
    data = pd.read_csv('data\nuevo_data.csv.csv')
    movie = data[data['title'] == titulo]
    return f"La película {movie['title'].values[0]} fue estrenada en el año {movie['release_year'].values[0]} con una puntuación/popularidad de {movie['popularity'].values[0]}"

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo):
    data = pd.read_csv('data\nuevo_data.csv.csv')
    movie = data[data['title'].str.lower() == titulo.lower()]

    if movie.empty:
        mensaje = f"No se encontró la película '{titulo}'."
    elif movie['vote_count'].values[0] >= 2000:
        mensaje = f"La película '{titulo}' fue estrenada en el año {movie['release_year'].values[0]}. La misma cuenta con un total de {movie['vote_count'].values[0]} valoraciones, con un promedio de {movie['vote_average'].values[0]}."
    else:
        mensaje = f"La película '{titulo}' no cumple con la condición mínima de 2000 valoraciones."

    return mensaje

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor):
    data_cred = pd.read_csv('data\new_cred.csv')
    data_nuevo = pd.read_csv('data\new_movies.csv.csv')

    actor_movies = data_cred[data_cred['actors'].str.contains(nombre_actor, case=False)]

    if actor_movies.empty:
        mensaje = f"No se encontró información para el actor '{nombre_actor}'."
    else:
        actor_success = data_nuevo[data_nuevo['id'].isin(actor_movies['id'])]['return'].sum()
        num_movies = len(actor_movies)
        avg_return = actor_success / num_movies if num_movies > 0 else 0.0

        mensaje = f"El actor '{nombre_actor}' ha participado en {num_movies} películas. El retorno total es {actor_success:.2f} con un promedio de {avg_return:.2f} por filmación."

    return mensaje

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director):
    data_cred = pd.read_csv('data\new_cred.csv.csv')
    data_movie = pd.read_csv('data\new_movies.csv')

    director_movies = data_cred[data_cred['director_names'] == nombre_director]

    if director_movies.empty:
        mensaje = f"No se encontró información para el director '{nombre_director}'."
    else:
        director_success = data_movie[data_movie['id'].isin(director_movies['id'])]['return'].sum()
        movies_details = data_movie[data_movie['id'].isin(director_movies['id'])][['title', 'release_date', 'return', 'budget', 'revenue']]

        peliculas = []
        for index, movie in movies_details.iterrows():
            pelicula = Pelicula(
                titulo=movie['title'],
                anio=movie['release_date'],
                retorno_pelicula=movie['return'],
                budget_pelicula=movie['budget'],
                revenue_pelicula=movie['revenue']
            )
            peliculas.append(pelicula)

        respuesta = {
            "director": nombre_director,
            "retorno_total_director": director_success,
            "peliculas": peliculas
        }

        mensaje = respuesta

    return mensaje



from utils import load_data, preprocess_data, compute_cosine_similarity
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo):
    df = load_data()
    df_processed = preprocess_data(df)
    df_indices, indices, cosine_sim = compute_cosine_similarity(df_processed)
    titulo= titulo.lower()
    indices_lower = {k.lower(): v for k, v in indices.items()}
    idx = indices_lower[titulo]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Obtener los 5 puntajes de similitud más altos
    movie_indices = [i[0] for i in sim_scores]
    top_movies = df_indices.iloc[movie_indices]['title'].tolist()  # Convertir los títulos en una lista de Python
    return top_movies