import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

movies = pd.read_csv('podatki/ml-latest-small/movies.csv')
ratings = pd.read_csv('podatki/ml-latest-small/ratings.csv')

merged_ratings = ratings.merge(movies[['movieId', 'title']], on='movieId')

rating_counts = merged_ratings['title'].value_counts()
valid_titles = rating_counts[rating_counts >= 2].index
filtered_ratings = merged_ratings[merged_ratings['title'].isin(valid_titles)]

films_sorted = rating_counts[rating_counts >= 2].sort_values(ascending=False).index.tolist()

st.set_page_config(page_title='Primerjava filmov', layout='wide')
st.title('Primerjava dveh filmov')

film1 = st.selectbox('Izberi prvi film:', films_sorted)
film2 = st.selectbox('Izberi drugi film:', films_sorted, index=1 if len(films_sorted) > 1 else 0)

ratings1 = filtered_ratings[filtered_ratings['title'] == film1]
ratings2 = filtered_ratings[filtered_ratings['title'] == film2]

st.subheader('Statistika ocen')
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**{film1}**")
    st.write(f"Povprečna ocena: {ratings1['rating'].mean():.2f}")
    st.write(f"Število ocen: {ratings1['rating'].count()}")
    st.write(f"Standardni odklon: {ratings1['rating'].std():.2f}")

with col2:
    st.markdown(f"**{film2}**")
    st.write(f"Povprečna ocena: {ratings2['rating'].mean():.2f}")
    st.write(f"Število ocen: {ratings2['rating'].count()}")
    st.write(f"Standardni odklon: {ratings2['rating'].std():.2f}")

st.subheader('Histogram ocen')
fig, axs = plt.subplots(1, 2, figsize=(10, 3), sharey=True)
axs[0].hist(ratings1['rating'], bins=np.arange(0.5, 5.5, 0.5))
axs[0].set_title(f'Ocene: {film1}')
axs[0].set_xlabel('Ocena')
axs[0].set_ylabel('Frekvenca')
axs[0].tick_params(labelsize=6)
axs[0].grid(True, alpha=0.4)

axs[1].hist(ratings2['rating'], bins=np.arange(0.5, 5.5, 0.5))
axs[1].set_title(f'Ocene: {film2}')
axs[1].set_xlabel('Ocena')
axs[1].tick_params(labelsize=6)
axs[1].grid(True, alpha=0.4)

plt.tight_layout()
st.pyplot(fig)

# Pridobi movieId za izbrana filma
id1 = movies[movies['title'] == film1]['movieId'].values[0]
id2 = movies[movies['title'] == film2]['movieId'].values[0]

ratings1 = ratings[ratings['movieId'] == id1].copy()
ratings2 = ratings[ratings['movieId'] == id2].copy()

ratings1.loc[:, 'year'] = pd.to_datetime(ratings1['timestamp'], unit='s').dt.year
ratings2.loc[:, 'year'] = pd.to_datetime(ratings2['timestamp'], unit='s').dt.year

avg_year1 = ratings1.groupby('year')['rating'].mean()
avg_year2 = ratings2.groupby('year')['rating'].mean()

count_year1 = ratings1.groupby('year')['rating'].count()
count_year2 = ratings2.groupby('year')['rating'].count()

st.subheader('Povprečna letna ocena in število ocen na leto')
fig2, axs2 = plt.subplots(1, 2, figsize=(10, 3))

axs2[0].plot(avg_year1.index, avg_year1.values, label=film1)
axs2[0].plot(avg_year2.index, avg_year2.values, label=film2)
axs2[0].set_title("Povprečna letna ocena", fontsize=6)
axs2[0].set_xlabel("Leto", fontsize=6)
axs2[0].set_ylabel("Povprečje", fontsize=6)
axs2[0].tick_params(labelsize=6)
axs2[0].legend(fontsize=6)
axs2[0].grid(True, alpha=0.4)

axs2[1].plot(count_year1.index, count_year1.values, label=film1)
axs2[1].plot(count_year2.index, count_year2.values, label=film2)
axs2[1].set_title("Število ocen na leto", fontsize=6)
axs2[1].set_xlabel("Leto", fontsize=6)
axs2[1].set_ylabel("Št. ocen", fontsize=6)
axs2[1].tick_params(labelsize=6)
axs2[1].legend(fontsize=6)
axs2[1].grid(True, alpha=0.4)

plt.tight_layout()
st.pyplot(fig2)
