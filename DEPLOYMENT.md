# Streamlit Cloud Deployment Guide 🚀

## Prerequisites
1. GitHub account
2. Streamlit Cloud account (free at share.streamlit.io)
3. OMDB API key (free at omdbapi.com)

## Step-by-Step Deployment

### 1. Prepare Your Repository
Your repository is already set up with the necessary files:
- `streamlit_app.py` - Main entry point for Streamlit Cloud
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - App configuration
- `.streamlit/secrets.toml` - Secrets template
- `src/` - Your application code

### 2. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Movie Recommendation App"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 3. Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit https://share.streamlit.io
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Connect your repository**:
   - Repository: `YOUR_USERNAME/YOUR_REPO_NAME`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. **Click "Deploy"**

### 4. Configure Secrets (Important!)

After deployment, you need to add your OMDB API key:

1. **In your Streamlit Cloud dashboard**, click on your app
2. **Click the "⚙️" (Settings) button**
3. **Go to "Secrets"**
4. **Add this configuration**:
```toml
[omdb]
api_key = "YOUR_ACTUAL_OMDB_API_KEY"
```
5. **Click "Save"**

### 5. Get Your OMDB API Key

1. Visit: http://www.omdbapi.com/apikey.aspx
2. Choose the FREE tier (1,000 requests/day)
3. Enter your email and verify
4. Copy your API key
5. Add it to Streamlit secrets (step 4 above)

## Important Notes

- **First deployment** may take 2-3 minutes as it processes the movie data
- **Subsequent visits** will be much faster
- **Free OMDB tier** allows 1,000 API calls per day
- **Sample dataset** is included for demo purposes
- **To use your full dataset**: Replace `src/sample_movies.csv` with your `movies.csv`

## Troubleshooting

### App won't start?
- Check that `streamlit_app.py` is in the root directory
- Verify all files are committed to GitHub
- Check the logs in Streamlit Cloud dashboard

### No posters showing?
- Verify OMDB API key is correctly set in secrets
- Check API key hasn't exceeded daily limit
- Try with popular movie titles first

### Preprocessing errors?
- Check that `sample_movies.csv` exists in `src/` folder
- Verify all required columns are present in CSV

## Your App URL
After deployment, your app will be available at:
`https://YOUR_APP_NAME.streamlit.app`

## Support
- Streamlit Docs: https://docs.streamlit.io
- OMDB API Docs: http://www.omdbapi.com