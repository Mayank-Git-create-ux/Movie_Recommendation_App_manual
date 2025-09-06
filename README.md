# Movie Recommendation System 🎬

A content-based movie recommendation system built using TF-IDF and cosine similarity. Built with Python and Streamlit for fast, interactive movie suggestions.

## Setup Instructions

### 1. Create Virtual Environment
Run the setup script to create and configure the virtual environment:
```bash
setup_venv.bat
```

### 2. Run the Application
Use the run script to start the app:
```bash
run_app.bat
```

### Manual Setup (Alternative)
If you prefer manual setup:
```bash
# Create virtual environment
python -m venv movie_app_env

# Activate virtual environment
movie_app_env\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run preprocessing
cd src
python preprocess.py

# Start the app
streamlit run main.py
```

## Features
- Content-based movie recommendations using TF-IDF vectorization
- Interactive Streamlit web interface
- Movie posters and plot summaries from OMDB API
- Cosine similarity for finding similar movies

## Requirements
- Python 3.7+
- All dependencies listed in requirements.txt
