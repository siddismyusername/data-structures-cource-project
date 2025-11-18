# Trie Streamlit App

This small project exposes the `Trie` implementation from `data-structure.py` via a Streamlit web UI.

Setup (Windows, cmd.exe):

1. Activate the provided virtual environment:

   ```cmd
   s:\project\data-structures\proj-env\Scripts\activate.bat
   ```

2. Install dependencies:

   ```cmd
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```cmd
   streamlit run streamlit_app.py
   ```

   If you see an error like `No module named streamlit`, ensure the venv is
   activated (step 1). Alternatively, run Streamlit with the venv’s Python:

   ```cmd
   s:\project\data-structures\proj-env\Scripts\python.exe -m streamlit run streamlit_app.py
   ```

   To use a custom port (e.g., if 8501 is taken):

   ```cmd
   s:\project\data-structures\proj-env\Scripts\python.exe -m streamlit run streamlit_app.py --server.port 8520
   ```

The app allows adding words, searching for full words, and checking prefixes. Words are stored in session state and will reset when the Streamlit session restarts.
