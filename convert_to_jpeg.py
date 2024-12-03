from PIL import Image
import os

def convert_to_jpeg(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.webp', '.png')):
            filepath = os.path.join(directory, filename)
            try:
                with Image.open(filepath) as img:
                    # Convert to RGB mode (required for JPEG)
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    
                    # Create new filename with .jpg extension
                    new_filename = os.path.splitext(filename)[0] + '.jpg'
                    new_filepath = os.path.join(directory, new_filename)
                    
                    # Save as JPEG with good quality
                    img.save(new_filepath, 'JPEG', quality=95)
                    
                    # If the new file is different from the original, delete the original
                    if new_filepath != filepath:
                        os.remove(filepath)
                    
                    print(f"Converted {filename} to JPEG")
            except Exception as e:
                print(f"Error converting {filename}: {str(e)}")

convert_to_jpeg('static/dmv_images')
