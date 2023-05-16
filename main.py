import pandas as pd
import streamlit as st
import pickle
import requests
import json

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

from bs4 import BeautifulSoup
from urllib.request import urlopen
import io

from scraper_api import ScraperAPIClient
client = ScraperAPIClient('a156500cd01cb7d1041dcae8e1836aa4')

st.title("Movie recommendation system")
def fetch_poster_Bollywood(imdb_link):
    ## Call to website using SDK
    url_data = client.get(imdb_link).text
    ## Fetch the site data
    s_data = BeautifulSoup(url_data, 'html.parser')
    ## Find the tag in which Image link is stored
    imdb_dp = s_data.find("meta", property="og:image")
    ## Get the URL of Image
    movie_poster_link = imdb_dp.attrs['content']

    return movie_poster_link

def recommend_Bollywood(option):
    index = bmovie[bmovie['title'] == option].index[0]
    distances = sorted(list(enumerate(bsimilarity[index])), reverse=True, key=lambda x: x[1])
    print("Recomending......")
    recommend_movies = []
    posters = []
    for i in distances[1:6]:
        movie_id=bmovie.imdbId.iloc[i[0]]
        imdb_link = "https://www.imdb.com/title/"+movie_id+"/?ref_=fn_tt_tt_1"
        recommend_movies.append(bmovie.iloc[i[0]].title)
        posters.append(fetch_poster_Bollywood(imdb_link))
    return recommend_movies,posters

bmovie_list = pickle.load(open("Bollywood.pkl","rb"))
bmovie = pd.DataFrame(bmovie_list)
bsimilarity = pickle.load(open("Bollywood_similarity.pkl","rb"))



def recommend(option):
    index = movie[movie['title'] == option].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movie.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movie.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


movie_list = pickle.load(open("Movies (1).pkl","rb"))
movie = pd.DataFrame(movie_list)
similarity = pickle.load(open("similarity.pkl","rb"))

genre = st.radio(
    "Select The Industry",
    ('Hollywood', 'Bollywood'))

if genre == 'Bollywood':
    op = st.selectbox(
        "Search for your movie : ",
        bmovie["title"])

    if st.button("Recommend"):
        recommendations, poster = recommend_Bollywood(op)
        cola, colb, colc, cold, cole = st.columns(5)
        with cola:
            st.write(recommendations[0])
            st.image(poster[0])
        with colb:
            st.write(recommendations[1])
            st.image(poster[1])
        with colc:
            st.write(recommendations[2])
            st.image(poster[2])
        with cold:
            st.write(recommendations[3])
            st.image(poster[3])
        with cole:
            st.write(recommendations[4])
            st.image(poster[4])


if genre == "Hollywood":
    option = st.selectbox(
            "Search for your movie : ",
            movie["title"])
    if st.button("Recommend.") :

            recommendations, poster = recommend(option)
            cola, colb, colc, cold, cole = st.columns(5)
            with cola:
                st.write(recommendations[0])
                st.image(poster[0])
            with colb:
                st.write(recommendations[1])
                st.image(poster[1])
            with colc:
                st.write(recommendations[2])
                st.image(poster[2])
            with cold:
                st.write(recommendations[3])
                st.image(poster[3])
            with cole:
                st.write(recommendations[4])
                st.image(poster[4])




