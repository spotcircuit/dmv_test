from PIL import Image
import os

def verify_images(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            filepath = os.path.join(directory, filename)
            try:
                with Image.open(filepath) as img:
                    print(f"{filename}: Valid image - Format: {img.format}, Size: {img.size}")
            except Exception as e:
                print(f"{filename}: Error - {str(e)}")

verify_images('static/dmv_images')
