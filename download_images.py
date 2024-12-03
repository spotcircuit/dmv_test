import os
import requests
from typing import Dict, Optional

class ImageDownloader:
    def __init__(self, save_dir: str = ".\\quiz_data\\images"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        
        # Dictionary mapping sign names to their public domain image URLs
        self.sign_images: Dict[str, str] = {
            "stop": "https://www.trafficsigns.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/r/1/r1-1.jpg",
            "yield": "https://www.trafficsigns.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/r/1/r1-2.jpg",
            "railroad_crossing": "https://www.trafficsigns.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/w/1/w10-1.jpg",
            "deer_crossing": "https://www.trafficsigns.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/w/1/w11-3.jpg",
            "schoolzonespeed": "https://www.trafficsigns.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/s/4/s4-3p.jpg",
            "hospital": "https://www.trafficsigns.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/d/9/d9-2.jpg",
            "steep_descent": "https://www.trafficsigns.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/w/7/w7-1.jpg",
            "no_uturn": "https://www.trafficsigns.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/r/3/r3-4.jpg",
            "two_way_traffic": "https://www.trafficsigns.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/w/6/w6-3.jpg"
        }

    def download_image(self, sign_name: str) -> Optional[str]:
        """Download an image and return its local path"""
        if sign_name not in self.sign_images:
            return None
            
        url = self.sign_images[sign_name]
        local_path = os.path.join(self.save_dir, f"{sign_name}.jpg")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.trafficsigns.com/'
            }
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return local_path
            
        except Exception as e:
            print(f"Error downloading {sign_name}: {str(e)}")
            return None

    def download_all_images(self) -> Dict[str, Optional[str]]:
        """Download all sign images and return mapping of names to local paths"""
        results = {}
        for sign_name in self.sign_images:
            results[sign_name] = self.download_image(sign_name)
        return results

if __name__ == "__main__":
    downloader = ImageDownloader()
    results = downloader.download_all_images()
    print("Downloaded images:")
    for sign, path in results.items():
        print(f"{sign}: {'Success' if path else 'Failed'}")
