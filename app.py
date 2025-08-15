import pickle
import streamlit as st
import requests
import pandas as pd
from streamlit_image_select import image_select
import time 

#  Helper Function to Fetch Movie Details & Poster from TMDB API 
def fetch_poster_and_details(movie_id):
    """Fetches movie poster URL and details from TMDB API using a movie ID."""
    try:
        # --- ADDED &language=en-US back to the URL ---
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=0d37b7e7118e5052df6ac15cc807e88e&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get('poster_path')
        full_poster_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750.png?text=No+Poster"

        details = {
            "title": data.get('title', 'N/A'),
            "overview": data.get('overview', 'No overview available.'),
            "release_date": data.get('release_date', 'N/A'),
            "rating": data.get('vote_average', 0),
            "genres": [genre['name'] for genre in data.get('genres', [])]
        }

        return full_poster_path, details
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return "https://via.placeholder.com/500x750.png?text=API+Error", {}

# --- Load Data ---
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Movie Recommendation System")

# --- App Header ---
st.title('Movie Recommendation System')
st.write("Select a movie from the dropdown to get recommendations.")

# --- Movie Selection Dropdown ---
selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values
)

# --- Recommendation Logic ---
if st.button('Show Recommendation', type="primary"):
    movie_index = movies[movies['title'] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    st.session_state['recommendations'] = []
    with st.spinner('Fetching recommendations...'):
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            title = movies.iloc[i[0]].title
            poster_url, details = fetch_poster_and_details(movie_id)
            st.session_state['recommendations'].append({
                "id": movie_id,
                "title": title,
                "poster_url": poster_url,
                "details": details
            })
            # --- ADDED THE DELAY TO PREVENT CONNECTION ERRORS ---
            time.sleep(0.2) 


# --- Display Clickable Recommendations ---
if 'recommendations' in st.session_state:
    st.subheader("Recommended Movies")

    posters = [rec["poster_url"] for rec in st.session_state.recommendations]
    captions = [rec["title"] for rec in st.session_state.recommendations]

    selected_poster = image_select(
        label="Click a poster to see the details",
        images=posters,
        captions=captions,
        use_container_width=False
    )
    
    if selected_poster:
        selected_movie_details = next(
            (rec for rec in st.session_state.recommendations if rec["poster_url"] == selected_poster),
            None
        )
        
        # ADDED CHECK: Make sure details dictionary is not empty before using it
        if selected_movie_details and selected_movie_details['details']:
            st.subheader(f"Details for: {selected_movie_details['details']['title']}")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(selected_movie_details["poster_url"])
            with col2:
                st.write(f"**Release Date:** {selected_movie_details['details']['release_date']}")
                st.write(f"**Rating:** {selected_movie_details['details']['rating']:.1f}/10 ⭐")
                st.write(f"**Genres:** {', '.join(selected_movie_details['details']['genres'])}")
                st.write("**Overview:**")
                st.write(selected_movie_details['details']['overview'])
        else:
            # Display a friendly message if details could not be fetched
            st.warning("Could not retrieve details for this movie due to a network error.")