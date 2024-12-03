import os
import shutil
from pathlib import Path

# Ensure static directory exists
static_dir = Path('static')
static_dir.mkdir(exist_ok=True)

# Ensure dmv_images directory exists
dmv_images_dir = static_dir / 'dmv_images'
dmv_images_dir.mkdir(exist_ok=True)

# Copy images from dmv_images directory to static/dmv_images
dmv_source_dir = Path('dmv_images')
if dmv_source_dir.exists():
    for file in dmv_source_dir.glob('*.jpg'):
        shutil.copy(file, dmv_images_dir / file.name)
    for file in dmv_source_dir.glob('*.png'):
        shutil.copy(file, dmv_images_dir / file.name)

# Create empty sound files if they don't exist
sound_files = ['correct.mp3', 'incorrect.mp3']
for sound_file in sound_files:
    sound_path = static_dir / sound_file
    if not sound_path.exists():
        sound_path.touch()
        print(f"Created empty {sound_file} - please add actual sound content")

print("Static files setup complete!")
