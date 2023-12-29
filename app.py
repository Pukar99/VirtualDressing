import streamlit as st
import os
from PIL import Image

# Initialize Streamlit app
st.title('Virtual Clothing Try-On')

# Widget for image upload
uploaded_file = st.file_uploader("Upload your image", type=['png', 'jpg', 'jpeg'])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

# Widget for selecting clothing items
clothing_options = ['Shirt', 'Pants', 'Dress', 'Skirt']
selected_clothing = st.selectbox("Select a clothing item to try on", clothing_options)

# Function to display images from the selected clothing folder
def display_clothing_images(selected_clothing):
    folder_path = f'./{selected_clothing.lower()}/'  # Folder name in lowercase
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                image_path = os.path.join(folder_path, file)
                image = Image.open(image_path)
                st.image(image, caption=file, width=250)
    else:
        st.write(f"No images found for {selected_clothing}.")

# Button to display clothing images
if st.button(f'Show {selected_clothing} options'):
    display_clothing_images(selected_clothing)
