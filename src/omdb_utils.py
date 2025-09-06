# omdb_utils.py
import requests
import re
from urllib.parse import quote

def clean_title_for_search(title):
    """Clean movie title for better OMDB API matching"""
    # Remove year in parentheses if present
    title = re.sub(r'\s*\(\d{4}\)', '', title)
    # Remove extra whitespace and special characters
    title = re.sub(r'[^\w\s-]', '', title)
    # Remove common prefixes/suffixes that might interfere
    title = re.sub(r'\b(The|A|An)\s+', '', title, flags=re.IGNORECASE)
    return title.strip()

def get_movie_details(title, api_key):
    """Get movie details from OMDB API with improved title matching"""
    
    # Try original title first
    titles_to_try = [title]
    
    # Add cleaned version
    cleaned_title = clean_title_for_search(title)
    if cleaned_title != title:
        titles_to_try.append(cleaned_title)
    
    # Try with "The" prefix if not present
    if not title.lower().startswith('the '):
        titles_to_try.append(f"The {title}")
    
    for search_title in titles_to_try:
        try:
            # URL encode the title to handle special characters
            encoded_title = quote(search_title)
            url = f"http://www.omdbapi.com/?t={encoded_title}&plot=full&apikey={api_key}"
            
            response = requests.get(url, timeout=5)
            res = response.json()
            
            if res.get("Response") == "True":
                plot = res.get("Plot", "N/A")
                poster = res.get("Poster", "N/A")
                
                # Check if poster URL is valid (not "N/A" and is a proper URL)
                if poster != "N/A" and poster.startswith("http"):
                    return plot, poster
                    
        except requests.RequestException:
            continue
    
    # If no results found, try a search instead of exact match
    try:
        search_url = f"http://www.omdbapi.com/?s={quote(cleaned_title)}&apikey={api_key}"
        response = requests.get(search_url, timeout=5)
        search_res = response.json()
        
        if search_res.get("Response") == "True" and "Search" in search_res:
            # Get the first result
            first_result = search_res["Search"][0]
            imdb_id = first_result.get("imdbID")
            
            if imdb_id:
                # Get details by IMDB ID
                detail_url = f"http://www.omdbapi.com/?i={imdb_id}&plot=full&apikey={api_key}"
                detail_response = requests.get(detail_url, timeout=5)
                detail_res = detail_response.json()
                
                if detail_res.get("Response") == "True":
                    plot = detail_res.get("Plot", "N/A")
                    poster = detail_res.get("Poster", "N/A")
                    
                    if poster != "N/A" and poster.startswith("http"):
                        return plot, poster
                        
    except requests.RequestException:
        pass
    
    return "N/A", "N/A"
