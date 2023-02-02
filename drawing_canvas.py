import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas


st.header("Handwritten Maths Equation Recognizer")

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("freedraw", "transform"), key='drawing_canvas_select_box'
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

realtime_update = st.sidebar.checkbox("Update in realtime", True)

    
st.write("Draw your equation here : ")
# Create a canvas component
canvas_result = st_canvas(
    #fill_color="rgba(0, 0, 0, 0)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=Image.open(bg_image) if bg_image else None,
    update_streamlit=realtime_update,
    height=300,
    width=1000,
    drawing_mode=drawing_mode,
    point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas",
)

submit_btn = st.button("Predict")





from predict import make_prediction

if canvas_result.image_data is not None and submit_btn:
    
    prediction = make_prediction(canvas_result.image_data)
    
    txt = (prediction)
    st.header("Prediction")
    txt_area = st.text_area('', txt)
    # print("Predicted Answer : ",prediction)
else:
    st.header("Prediction")
    txt_area = st.text_area('', "")


if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
    st.dataframe(objects)

