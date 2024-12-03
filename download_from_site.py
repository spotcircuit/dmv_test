import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time
from PIL import Image as PILImage
import io
import random

def download_with_retry(url, headers, max_retries=3, base_delay=2):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:  # Too Many Requests
                delay = base_delay * (attempt + 1) + random.uniform(0, 1)
                print(f"Rate limit hit, waiting {delay:.1f} seconds...")
                time.sleep(delay)
                continue
            else:
                print(f"Failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(base_delay)
            continue
    return None

def download_images():
    # Browser-like headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://permittestpractice.com/virginia/road-signs/',
    }

    base_url = 'https://permittestpractice.com'
    page_url = urljoin(base_url, '/virginia/road-signs/')
    
    # Create directory if it doesn't exist
    save_dir = 'static/dmv_images'
    os.makedirs(save_dir, exist_ok=True)
    
    # Get the page with retry
    response = download_with_retry(page_url, headers)
    if not response:
        print("Failed to fetch the main page")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    print(f"Found {len(images)} images")
    
    # Track existing files
    existing_files = set(os.listdir(save_dir))
    print("\nExisting files that will be replaced:")
    for file in existing_files:
        print(f"- {file}")
    
    for img in images:
        src = img.get('src')
        alt = img.get('alt', '')
        
        if not src or 'logo' in src.lower():
            continue
            
        full_url = urljoin(base_url, src)
        filename = os.path.basename(src)
        base_filename = os.path.splitext(filename)[0]
        jpg_filename = base_filename + '.jpg'
        
        print(f"\nProcessing: {alt} ({full_url})")
        
        # Add a random delay between requests
        time.sleep(random.uniform(1.5, 3.0))
        
        try:
            img_response = download_with_retry(full_url, headers)
            if img_response:
                # Convert to JPG using PIL
                img_data = io.BytesIO(img_response.content)
                img = PILImage.open(img_data)
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if needed
                if img.width > 800 or img.height > 800:
                    img.thumbnail((800, 800), PILImage.Resampling.LANCZOS)
                
                # Save as JPG
                save_path = os.path.join(save_dir, jpg_filename)
                if os.path.exists(save_path):
                    os.remove(save_path)
                img.save(save_path, 'JPEG', quality=95)
                print(f"Saved: {jpg_filename}" + (" (replaced existing file)" if jpg_filename in existing_files else ""))
            else:
                print(f"Failed to download image after retries")
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue

if __name__ == "__main__":
    download_images()
