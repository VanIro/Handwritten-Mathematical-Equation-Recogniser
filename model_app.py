import streamlit as st
import keras
from keras.utils.vis_utils import plot_model
import visualkeras

from PIL import Image

model = keras.models.load_model('./models/model2OvSampled.keras')

tab1, tab2, tab3 = st.tabs(["Model Visualization", "Stats", "Upload & Use Custom Model"]) #this order is the order in the tab navigations


with tab1:
    visualkeras.layered_view(model, legend=True) # without custom font
    from PIL import ImageFont
    font = ImageFont.truetype("arial.ttf", 12)
    image = visualkeras.layered_view(model, legend=True, font=font) # selected font
    st.image(image)

    #plot_model(model, to_file='./model_viz_images/model_plot.png', show_shapes=True, show_layer_names=True)

    image = Image.open('./model_viz_images/model_plot.png')

    st.image(image, caption='Plot of the model Architecture')

with tab2:
    image = Image.open('./stats_figure/dataset.png')
    st.image(image, caption='Classes Size in the dataset')

    image2 = Image.open('./stats_figure/train_accuracy.png')
    st.image(image2, caption='Accuracy of model for each class in training set')

    image3 = Image.open('./stats_figure/train_val_errors_vs_epoch.png')
    st.image(image3, caption='Accuracy of model for each class in training set')

with tab3:
    custom_model = st.sidebar.file_uploader("Custom Keras Model", type=["keras"], key="model_uploader")
    custom_labels = st.sidebar.file_uploader("Label Mappings for Your Model [json for python dict]", type=["json"], key="label_mapping_file_uploader")

    mapping_label = None

    model_pars = None
    
    st.header("Custom Model")

    if custom_model is not None:
        if custom_labels is not None:
            with open("./user_uploads/model.keras","wb") as file:
                file.write(custom_model.getvalue())

            import json
            mapping_labels = json.load(custom_labels)

            model_pars = dict()
            model_pars["model"] = keras.models.load_model("./user_uploads/model.keras"),
            model_pars["mapping"] = mapping_labels
            
            st.subheader("Custom Model and mapping loaded")

    with st.container():
        exec(open(f"./drawing_canvas.py").read())


