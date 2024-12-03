from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import logging
import time
import os
import requests
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_angular(driver):
    """Wait for Angular to finish loading"""
    script = """
    try {
        if (window.getAllAngularTestabilities) {
            return window.getAllAngularTestabilities().findIndex(x => !x.isStable()) === -1;
        }
        return true;
    } catch (e) {
        return true;
    }
    """
    return driver.execute_script(script)

def save_image(url, folder):
    """Save an image from URL to the specified folder"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = url.split('/')[-1]
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filename
    except Exception as e:
        logger.error(f"Error saving image {url}: {str(e)}")
    return None

def test_scrape():
    # Initialize Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Create output directories
    image_dir = "dmv_images"
    os.makedirs(image_dir, exist_ok=True)
    
    try:
        # Go to main page
        url = "https://transactions.dmv.virginia.gov/dmv-manuals/#/"
        logger.info(f"Accessing URL: {url}")
        
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        
        # Wait for Angular to load
        time.sleep(5)
        logger.info("Waiting for Angular...")
        WebDriverWait(driver, 10).until(wait_for_angular)
        logger.info("Angular loaded")
        
        try:
            # First find and click the Driver's Study Guide
            logger.info("Looking for Driver's Study Guide...")
            guide_xpath = "//b[contains(text(), 'Driver')]"
            guide = wait.until(
                EC.element_to_be_clickable((By.XPATH, guide_xpath))
            )
            logger.info("Found Driver's Study Guide, clicking...")
            driver.execute_script("arguments[0].click();", guide)
            logger.info("Clicked Driver's Study Guide")
            
            # Wait for content to load
            time.sleep(5)
            WebDriverWait(driver, 10).until(wait_for_angular)
            
            # Now find and click Section 2
            logger.info("Looking for Section 2...")
            section_xpath = "//p[contains(text(), 'Signals, Signs')]"
            section = wait.until(
                EC.element_to_be_clickable((By.XPATH, section_xpath))
            )
            logger.info("Found Section 2, clicking...")
            driver.execute_script("arguments[0].click();", section)
            logger.info("Clicked Section 2")
            
            # Wait for content to load
            time.sleep(5)
            WebDriverWait(driver, 10).until(wait_for_angular)
            
            # Extract content
            content_data = {
                'title': 'Signals, Signs and Pavement Markings',
                'content': [],
                'images': []
            }
            
            # Try to find content paragraphs
            logger.info("Looking for content...")
            paragraphs = driver.find_elements(By.TAG_NAME, "p")
            for p in paragraphs:
                text = p.text.strip()
                if text:
                    content_data['content'].append(text)
            logger.info(f"Found {len(content_data['content'])} paragraphs")
            
            # Look for images
            logger.info("Looking for images...")
            images = driver.find_elements(By.TAG_NAME, "img")
            logger.info(f"Found {len(images)} images")
            
            for img in images:
                src = img.get_attribute("src")
                alt = img.get_attribute("alt")
                if src:
                    # Convert relative URLs to absolute
                    if not src.startswith('http'):
                        src = f"https://transactions.dmv.virginia.gov{src}"
                    
                    # Save image
                    filename = save_image(src, image_dir)
                    if filename:
                        content_data['images'].append({
                            'filename': filename,
                            'alt': alt,
                            'url': src
                        })
                        logger.info(f"Saved image: {filename}")
            
            # Save content data
            with open('section2_content.json', 'w', encoding='utf-8') as f:
                json.dump(content_data, f, indent=2)
            logger.info("Saved content data to section2_content.json")
            
        except Exception as e:
            logger.error(f"Error during navigation: {str(e)}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        driver.quit()
        logger.info("Browser closed")

if __name__ == "__main__":
    test_scrape()
