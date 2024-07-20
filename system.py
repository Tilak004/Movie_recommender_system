import pandas as pd
import streamlit as st
import requests
import pickle
# Title for the web page
st.title('Movies Recommender System')
movies_dict1 = pickle.load(open('movies_dict1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict1)

similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=94de473e012f219146c90a472a6862da&language=en-US'.format(movie_id))
        data = response.json()
        return "http://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies=[]
        recommended_movies_posters=[]
        for i in movies_list:
                movie_id = movies.iloc[i[0]].movie_id
                recommended_movies.append(movies.iloc[i[0]].title)
                # fetch poster from API
                recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies,recommended_movies_posters

# Creating the select box
selected_movie_name = st.selectbox(
        'What movies you want to watch?',
        movies['title'].values
)
# Creating a button
if st.button('Recommend'):
        names,posters = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
                st.text(names[0])
                st.image(posters[0])
        with col2:
                st.text(names[1])
                st.image(posters[1])
        with col3:
                st.text(names[2])
                st.image(posters[2])
        with col4:
                st.text(names[3])
                st.image(posters[3])
        with col5:
                st.text(names[4])
                st.image(names[4])
