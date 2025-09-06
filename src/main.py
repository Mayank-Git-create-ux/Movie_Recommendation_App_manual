# app.py
import json
import os
import streamlit as st
from recommend import df, recommend_movies
from omdb_utils import get_movie_details

# Load OMDB API key - works both locally and on Streamlit Cloud
try:
    # Try Streamlit secrets first (for cloud deployment)
    OMDB_API_KEY = st.secrets["omdb"]["api_key"]
except (KeyError, FileNotFoundError):
    # Fallback to local config file
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        OMDB_API_KEY = config["OMDB_API_KEY"]
    except FileNotFoundError:
        st.error("⚠️ API key not found. Please configure OMDB API key in Streamlit secrets or config.json")
        st.info("Get a free API key from: http://www.omdbapi.com/apikey.aspx")
        st.stop()

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommender")

# Using 'title' instead of 'song' now
movie_list = sorted(df['title'].dropna().unique())
selected_movie = st.selectbox("🎬 Select a movie:", movie_list)

if st.button("🚀 Recommend Similar Movies"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        if recommendations is None or recommendations.empty:
            st.warning("Sorry, no recommendations found.")
        else:
            st.success("Top similar movies:")
            for _, row in recommendations.iterrows():
                movie_title = row['title']
                
                with st.spinner(f"Loading details for {movie_title}..."):
                    plot, poster = get_movie_details(movie_title, OMDB_API_KEY)

                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A" and poster.startswith("http"):
                            try:
                                st.image(poster, width=100, caption="")
                            except Exception as e:
                                st.write("🖼️ Poster unavailable")
                        else:
                            # Show a placeholder instead of error message
                            st.markdown("""
                            <div style='width: 100px; height: 150px; background: linear-gradient(45deg, #f0f0f0, #e0e0e0); 
                                        border: 2px dashed #ccc; display: flex; align-items: center; justify-content: center;
                                        border-radius: 8px; font-size: 24px;'>
                                🎬
                            </div>
                            """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"### {movie_title}")
                        if plot != "N/A":
                            st.markdown(f"*{plot}*")
                        else:
                            st.markdown("_Plot not available_")
                        
                        # Add a small debug info (can be removed later)
                        if poster == "N/A":
                            st.caption("💡 Tip: Some movies may not have posters in the database")
