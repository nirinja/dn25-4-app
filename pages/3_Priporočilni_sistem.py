import streamlit as st
import hashlib
import json
import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('podatki/ml-latest-small/movies.csv')
ratings_df = pd.read_csv('podatki/ml-latest-small/ratings.csv')

USERS_FILE = '../users.json'
USER_RATINGS_FILE = '../ratings_user.json'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def load_user_ratings():
    if os.path.exists(USER_RATINGS_FILE):
        with open(USER_RATINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_ratings(user_ratings):
    with open(USER_RATINGS_FILE, 'w') as f:
        json.dump(user_ratings, f)

users = load_users()
user_ratings_data = load_user_ratings()

if 'user' not in st.session_state:
    st.session_state.user = None

st.title("Sistem za priporočanje filmov")

if st.session_state.user:
    st.success(f"Prijavljena kot: {st.session_state.user}")
    if st.button("Odjava"):
        st.session_state.user = None
        st.rerun()
else:
    tab1, tab2 = st.tabs(["Prijava", "Registracija"])

    with tab1:
        username = st.text_input("Uporabniško ime", key="login_user")
        password = st.text_input("Geslo", type="password", key="login_pass")
        if st.button("Prijavi se"):
            if username in users and users[username] == hash_password(password):
                st.session_state.user = username
                st.success("Prijava uspešna.")
                st.rerun()
            else:
                st.error("Napačno uporabniško ime ali geslo.")

    with tab2:
        new_user = st.text_input("Novo uporabniško ime", key="reg_user")
        new_pass = st.text_input("Novo geslo", type="password", key="reg_pass")
        if st.button("Registriraj se"):
            if new_user in users:
                st.error("Uporabnik že obstaja.")
            else:
                users[new_user] = hash_password(new_pass)
                save_users(users)
                st.success("Registracija uspešna.")

if st.session_state.user:
    user_ratings = user_ratings_data.get(st.session_state.user, {})
    st.header("Ocenjevanje filmov")

    ocenjeni_id = [int(i) for i in user_ratings.keys()]
    neocenjeni_filmi = movies[~movies['movieId'].isin(ocenjeni_id)]

    if neocenjeni_filmi.empty:
        st.info("Ocenila si že vse filme. Hvala!")
    else:
        film = st.selectbox("Izberi film", neocenjeni_filmi['title'].tolist())
        film_id = neocenjeni_filmi[neocenjeni_filmi['title'] == film]['movieId'].values[0]
        ocena = st.slider("Tvoja ocena", 0, 5, 3, 1)

        if st.button("Shrani oceno"):
            user_ratings[str(film_id)] = ocena
            user_ratings_data[st.session_state.user] = user_ratings
            save_user_ratings(user_ratings_data)
            st.success("Ocena shranjena.")
            st.rerun()

    if user_ratings:
        st.subheader("Tvoje ocene:")
        ocene_df = pd.DataFrame([
            {"film": movies[movies['movieId'] == int(fid)]['title'].values[0], "ocena": oc}
            for fid, oc in user_ratings.items()
        ])
        st.dataframe(ocene_df)

    if len(user_ratings) >= 10:
        st.header("Priporočila")
        if st.button("Priporoči mi filme"):
            all_ratings = ratings_df[['userId', 'movieId', 'rating']].copy()

            new_user_id = 99999
            for mid_str, oc in user_ratings.items():
                all_ratings = pd.concat([all_ratings, pd.DataFrame([{
                    'userId': new_user_id,
                    'movieId': int(mid_str),
                    'rating': oc
                }])])

            matrix = all_ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

            similarities = cosine_similarity(matrix)
            sim_df = pd.DataFrame(similarities, index=matrix.index, columns=matrix.index)

            podobni = sim_df.loc[new_user_id].drop(new_user_id).sort_values(ascending=False)

            priporocila = {}

            for podobni_id in podobni.index:
                teza = podobni[podobni_id]
                for mid, ocena in matrix.loc[podobni_id].items():
                    if matrix.loc[new_user_id, mid] == 0 and ocena > 3.5:
                        priporocila[mid] = priporocila.get(mid, 0) + ocena * teza

            if priporocila:
                top10 = sorted(priporocila.items(), key=lambda x: x[1], reverse=True)[:10]
                for mid, score in top10:
                    naslov = movies[movies['movieId'] == mid]['title'].values[0]
                    st.write(f"{naslov} (priporočilna ocena: {score/10:.2f})")
            else:
                st.info("Ni zadostnih podatkov za priporočila.")
    else:
        st.info("Za priporočila moraš oceniti vsaj 10 filmov.")
