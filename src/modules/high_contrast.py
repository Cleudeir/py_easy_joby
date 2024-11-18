import cv2
import numpy as np
from PIL import Image
import os

def enhance_letters(img_path, output_dir):
    """
    Enhance letters in an image to improve visibility for OCR and save intermediate transformations.

    Args:
        img_path (str): Path to the input image.
        output_dir (str): Directory to save the intermediate and final images.

    Returns:
        PIL.Image: Image with enhanced letters.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the image using OpenCV
    img = cv2.imread(img_path)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"{output_dir}/01_grayscale.png", gray_img)
    
    # Apply enchented letters
    enc=cv2.Laplacian(img, cv2.CV_8UC4, ksize=3)
    cv2.imwrite(f"{output_dir}/02_enhanced_letters.png", enc)
    # Convert the binary image to a PIL image
    final_image = Image.fromarray(enc)

    # Save the final processed image
    final_image.save(f"{output_dir}/04_final_enhanced_image.png")

    return final_image
