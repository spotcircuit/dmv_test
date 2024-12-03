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
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
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

def scrape_section_content(driver, wait):
    """Extract content and images from the current section"""
    content_data = {
        'content': [],
        'images': []
    }
    
    # Wait for content to load
    time.sleep(5)
    WebDriverWait(driver, 10).until(wait_for_angular)
    
    try:
        # Get section title
        title_elem = driver.find_element(By.CSS_SELECTOR, "h1, h2, h3")
        content_data['title'] = title_elem.text.strip()
    except:
        content_data['title'] = "Untitled Section"
    
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
            filename = save_image(src, "dmv_images")
            if filename:
                content_data['images'].append({
                    'filename': filename,
                    'alt': alt,
                    'url': src
                })
                logger.info(f"Saved image: {filename}")
    
    return content_data

def scrape_dmv_manual():
    """Scrape all sections of the DMV manual"""
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
    os.makedirs("dmv_images", exist_ok=True)
    os.makedirs("dmv_content", exist_ok=True)
    
    manual_data = {
        'title': "Virginia Driver's Manual",
        'date_scraped': datetime.now().isoformat(),
        'sections': []
    }
    
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
        
        # First find and click the Driver's Study Guide
        logger.info("Looking for Driver's Study Guide...")
        guide_xpath = "//b[contains(text(), 'Driver')]"
        guide = wait.until(
            EC.element_to_be_clickable((By.XPATH, guide_xpath))
        )
        logger.info("Found Driver's Study Guide, clicking...")
        driver.execute_script("arguments[0].click();", guide)
        logger.info("Clicked Driver's Study Guide")
        
        # Wait for sections to load
        time.sleep(5)
        WebDriverWait(driver, 10).until(wait_for_angular)
        
        # Find all section panels
        section_panels = driver.find_elements(By.XPATH, "//div[contains(@class, 'panel')]//p")
        logger.info(f"Found {len(section_panels)} sections")
        
        # Store section titles for navigation
        sections = []
        for panel in section_panels:
            text = panel.text.strip()
            if text:
                sections.append(text)
        
        # Process each section
        for i, section_title in enumerate(sections, 1):
            logger.info(f"Processing section {i}: {section_title}")
            
            try:
                # Find and click section
                section_xpath = f"//p[contains(text(), '{section_title}')]"
                section = wait.until(
                    EC.element_to_be_clickable((By.XPATH, section_xpath))
                )
                driver.execute_script("arguments[0].click();", section)
                
                # Scrape section content
                content = scrape_section_content(driver, wait)
                content['section_number'] = i
                content['section_title'] = section_title
                
                # Save section content
                section_file = f"dmv_content/section_{i}.json"
                with open(section_file, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2)
                logger.info(f"Saved section content to {section_file}")
                
                # Add to manual data
                manual_data['sections'].append({
                    'number': i,
                    'title': section_title,
                    'file': section_file
                })
                
                # Go back to sections list
                driver.execute_script("window.history.go(-1)")
                time.sleep(3)
                WebDriverWait(driver, 10).until(wait_for_angular)
                
            except Exception as e:
                logger.error(f"Error processing section {section_title}: {str(e)}")
                continue
        
        # Save manual index
        with open('dmv_content/manual_index.json', 'w', encoding='utf-8') as f:
            json.dump(manual_data, f, indent=2)
        logger.info("Saved manual index to manual_index.json")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        driver.quit()
        logger.info("Browser closed")

if __name__ == "__main__":
    scrape_dmv_manual()
