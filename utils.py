# utils.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

'''# Variables globales
indices = None
cosine_sim = None'''
m = None
C= None

def load_data():
    df = pd.read_csv('movies.csv')
    df = df[['title', 'vote_average','overview','vote_count','popularity']]
    df.to_csv('moviesml.csv', index=False)
    return pd.read_csv('moviesml.csv')



def weighted_rating(x):
    global C
    global m
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

def preprocess_data(df):
    global C
    global m
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    
    C = vote_averages.mean()
    m = vote_counts.quantile(0.95)
    qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][['title', 'vote_average', 'overview', 'vote_count','popularity']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    return qualified

def compute_cosine_similarity(df):
    ''''global indices, cosine_sim'''
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df['overview'].fillna(''))
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['title'])
    return df.reset_index(), indices, cosine_sim


def recomendacion(titulo,df_indices,indices, cosine_sim):
   
    idx = indices[titulo]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Obtener los 5 puntajes de similitud más altos
    movie_indices = [i[0] for i in sim_scores]
    top_movies = df_indices.iloc[movie_indices]['title'].tolist()  # Convertir los títulos en una lista de Python
    return top_movies


df = load_data()
qualified = preprocess_data(df)
df_indices, indices, cosine_sim = compute_cosine_similarity(qualified)
top_movies= recomendacion('Toy Story',df_indices,indices, cosine_sim )
print (top_movies)