#!/usr/bin/env python3
"""
Test script to verify OMDB API functionality
"""
import json
import os
from omdb_utils import get_movie_details

def test_omdb_api():
    # Load config
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config.json")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    api_key = config["OMDB_API_KEY"]
    
    # Test with popular movies
    test_movies = [
        "The Shawshank Redemption",
        "The Godfather", 
        "Pulp Fiction",
        "The Dark Knight",
        "Forrest Gump"
    ]
    
    print("Testing OMDB API...")
    print("=" * 50)
    
    for movie in test_movies:
        print(f"\nTesting: {movie}")
        plot, poster = get_movie_details(movie, api_key)
        
        print(f"Plot: {'✅ Found' if plot != 'N/A' else '❌ Not found'}")
        print(f"Poster: {'✅ Found' if poster != 'N/A' and poster.startswith('http') else '❌ Not found'}")
        
        if poster != "N/A":
            print(f"Poster URL: {poster}")

if __name__ == "__main__":
    test_omdb_api()