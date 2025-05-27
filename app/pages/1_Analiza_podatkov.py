import pandas as pd
import numpy as np
import streamlit as st

# Naložimo podatke
movies = pd.read_csv('../podatki/ml-latest-small/movies.csv')
ratings = pd.read_csv('../podatki/ml-latest-small/ratings.csv')

# Razdelimo naslov in leto
movies['year'] = movies['title'].str.extract(r'\((\d{4})\)').astype('Int64')
movies['title_clean'] = movies['title'].str.replace(r'\(\d{4}\)', '', regex=True).str.strip()

# Ločimo žanre v seznam
movies['genres'] = movies['genres'].str.split('|')

# Združimo ocene
average_ratings = ratings.groupby('movieId').agg({'rating': ['mean', 'count']}).reset_index()
average_ratings.columns = ['movieId', 'average_rating', 'num_ratings']

# Združimo z naslovom, letom in žanri
merged = pd.merge(average_ratings, movies[['movieId', 'title_clean', 'year', 'genres']], on='movieId')

# Streamlit nastavitve
st.set_page_config(page_title='Analiza filmov', layout='wide')
st.title('1 Analiza filmov')

max_ratings = merged['num_ratings'].max()
min_ratings = st.slider('Minimalno število ocen:', min_value=1, max_value=int(max_ratings), value=10, step=1)

# Pridobimo žanre
all_genres = sorted(set(g for genre_list in movies['genres'].dropna() for g in genre_list))
selected_genre = st.selectbox('Izberi žanr (opcijsko):', ['Vsi'] + all_genres)

all_years = sorted(movies['year'].dropna().unique(), reverse=True)
selected_year = st.selectbox('Izberi leto (opcijsko):', ['Vsa leta'] + list(all_years))

# Filtriranje glede na izbrane filtre
filtered = merged[merged['num_ratings'] >= min_ratings]

if selected_genre != 'Vsi':
    filtered = filtered[filtered['genres'].apply(lambda x: selected_genre in x)]

if selected_year != 'Vsa leta':
    filtered = filtered[filtered['year'] == selected_year]

# Prikaz top 10
top_10 = filtered.sort_values('average_rating', ascending=False).head(10)

st.subheader('Top 10 filmov po povprečni oceni')
st.dataframe(top_10[['title_clean', 'average_rating', 'num_ratings', 'year']].rename(columns={
    'title_clean': 'Naslov',
    'average_rating': 'Povprečna ocena',
    'num_ratings': 'Število ocen',
    'year': 'Leto'
}))
