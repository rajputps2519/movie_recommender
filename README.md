# 🎬 Movie Recommender System

A content-based movie recommender system built with Python and Streamlit. This application suggests movies similar to a user's selection based on plot, genres, cast, and crew.
Click here for open live app
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movierecommender-fxzcfnibczmj2rcsutjcca.streamlit.app/)
App screenshot 
![App Screenshot](https://github.com/rajputps2519/movie_recommender/blob/main/Screenshot%202025-08-16%20042701.png?raw=true)

## ✨ Features

* **Content-Based Filtering**: Recommends movies by analyzing textual features like plot, genres, keywords, cast, and director.
* **Interactive UI**: A user-friendly web interface built with Streamlit where users can select a movie from a dropdown menu.
* **Dynamic Details**: Fetches and displays movie posters, overviews, ratings, and genres in real-time using the TMDB API.
* **Clickable Posters**: Recommended movie posters are clickable, allowing users to instantly view details for any suggested movie.

## ⚙️ How It Works

The recommendation engine is built using a content-based filtering approach:
1.  **Data Preprocessing**: The initial datasets from TMDB are cleaned and merged. Key features (overview, genres, keywords, cast, crew) are extracted.
2.  **Feature Engineering**: A "tags" vector is created for each movie by combining all its textual features into a single string.
3.  **Vectorization**: The text data in the "tags" is converted into a numerical vector space using the `CountVectorizer` (Bag-of-Words model).
4.  **Similarity Calculation**: The cosine similarity is calculated between all movie vectors to determine how similar each movie is to every other movie.
5.  **Recommendation**: When a user selects a movie, the system finds the 5 movies with the highest cosine similarity scores and recommends them.

## 🛠️ Tech Stack

* **Backend & Model**: Python, Pandas, NumPy, Scikit-learn, NLTK
* **Frontend**: Streamlit
* **Data**: The Movie Database (TMDB) API

## 🚀 Setup and Installation

Follow these steps to run the project on your local machine.

### 1. Prerequisites
* Python 3.8 or later
* Git

### 2. Clone the Repository
```bash
git clone [https://github.com/rajputps2519/movie_recommender.git](https://github.com/rajputps2519/movie_recommender.git)
cd movie_recommender
