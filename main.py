import streamlit as st

import drawing_canvas, model_app

# Define pages based on apps imported.
PAGES = {
    "Draw & Predict": "drawing_canvas",
    "Model": "model_app"
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()),key="Navigation")
page = PAGES[selection]

exec(open(f"./{page}.py").read())