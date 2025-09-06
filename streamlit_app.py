# Main entry point for Streamlit Cloud
import sys
import os
import subprocess
import streamlit as st

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

# Check if preprocessed files exist, if not run preprocessing
pkl_files = ['df_cleaned.pkl', 'cosine_sim.pkl', 'tfidf_matrix.pkl']
pkl_paths = [os.path.join(src_dir, f) for f in pkl_files]

if not all(os.path.exists(path) for path in pkl_paths):
    with st.spinner("🔄 Setting up movie recommendation system... This may take a moment on first run."):
        try:
            # Run preprocessing
            preprocess_path = os.path.join(src_dir, 'preprocess.py')
            subprocess.run([sys.executable, preprocess_path], cwd=src_dir, check=True)
            st.success("✅ Setup complete!")
        except subprocess.CalledProcessError as e:
            st.error(f"❌ Setup failed: {e}")
            st.stop()

# Import and run the main app
exec(open(os.path.join(src_dir, 'main.py')).read())