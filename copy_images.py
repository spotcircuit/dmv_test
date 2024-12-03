import shutil
import os
from pathlib import Path

src_dir = Path('quiz_data/images')
dst_dir = Path('static/dmv_images')

# Create destination directory if it doesn't exist
dst_dir.mkdir(parents=True, exist_ok=True)

# Copy all images
for img_file in src_dir.glob('*.jpg'):
    shutil.copy2(img_file, dst_dir / img_file.name)
    print(f"Copied {img_file.name}")
