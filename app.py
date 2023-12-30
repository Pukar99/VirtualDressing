from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import cv2
import numpy as np

# # Load environment variables
# load_dotenv()
# api_key = os.getenv('GEMINI_API_KEY')  # If needed for future use with Gemini API

# Initialize Streamlit app
st.title('Virtual Clothing Try-On')

# Widget for image upload
uploaded_file = st.file_uploader("Upload your image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Convert the uploaded file to an image
    person_image = Image.open(uploaded_file)
    person_image_cv2 = np.array(person_image)
    person_image_cv2 = person_image_cv2[:, :, ::-1].copy()  # Convert RGB to BGR for OpenCV
    st.image(person_image_cv2, caption='Uploaded Image', use_column_width=True)

# Function to overlay clothing on the person
def overlay_clothing(person_image, clothing_image_path):
    clothing_image = cv2.imread(clothing_image_path, cv2.IMREAD_UNCHANGED)
    scale_percent = 50  # Resize percentage, adjust as needed
    width = int(clothing_image.shape[1] * scale_percent / 100)
    height = int(clothing_image.shape[0] * scale_percent / 100)
    resized_clothing = cv2.resize(clothing_image, (width, height), interpolation=cv2.INTER_AREA)
    
    # Assume the clothing should be placed in the middle of the person's image
    x_offset = (person_image.shape[1] - resized_clothing.shape[1]) // 2
    y_offset = (person_image.shape[0] - resized_clothing.shape[0]) // 2
    
    # Create a mask and inverse mask from the resized clothing image
    clothing_alpha_channel = resized_clothing[:, :, 3]
    _, mask = cv2.threshold(clothing_alpha_channel, 1, 255, cv2.THRESH_BINARY)
    inverse_mask = cv2.bitwise_not(mask)
    
    # Region of interest from the person's image where the clothing will be placed
    roi = person_image[y_offset:y_offset+height, x_offset:x_offset+width]
    
    # Use the masks to add the clothing to the person's image
    person_no_clothing = cv2.bitwise_and(roi, roi, mask=inverse_mask)
    clothing_with_alpha = cv2.bitwise_and(resized_clothing, resized_clothing, mask=mask)
    
    # Combine the person image without the clothing area and the clothing image
    final_roi = cv2.add(person_no_clothing, clothing_with_alpha[:, :, :3])
    
    # Update the original person image with the final ROI that includes the clothing
    person_image[y_offset:y_offset+height, x_offset:x_offset+width] = final_roi
    return person_image

# Widget for selecting clothing items
clothing_options = ['Shirt', 'Pants', 'Dress', 'Skirt']
selected_clothing = st.selectbox("Select a clothing item to try on", clothing_options)

# Button to try on selected clothing
if st.button(f'Try on {selected_clothing}'):
    # Path to the directory containing clothing images
    folder_path = f'./{selected_clothing.lower()}/'
    if os.path.isdir(folder_path):
        # List PNG images in the folder
        clothing_images = [img for img in os.listdir(folder_path) if img.endswith('.png')]
        if clothing_images:
            # For simplicity, take the first image in the folder
            clothing_image_path = os.path.join(folder_path, clothing_images[0])
            # Overlay the clothing and display the result
            final_image = overlay_clothing(person_image_cv2, clothing_image_path)
            st.image(final_image, caption=f'{selected_clothing} Try-On', channels="BGR", use_column_width=True)
        else:
            st.error(f"No images found in the {selected_clothing} folder.")
    else:
        st.error(f"The {selected_clothing} folder does not exist.")
