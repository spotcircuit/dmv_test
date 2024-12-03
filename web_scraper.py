import requests
import json
import os
from bs4 import BeautifulSoup
import logging
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class DMVManualScraper:
    def __init__(self, debug=False):
        self.debug = debug
        self.base_url = "https://transactions.dmv.virginia.gov/dmv-manuals/#/manual/1/section"
        self.quiz_base_url = "https://transactions.dmv.virginia.gov/dmv-manuals/#/manual/1/quiz"  # For future use
        self.sections = {
            2: {"name": "Signs, Signals and Markings", "subsections": ["2.1", "2.2", "2.3", "2.4"]},
            3: {"name": "Safe Driving", "subsections": ["3.1", "3.2", "3.3"]},
            4: {"name": "Traffic Laws", "subsections": ["4.1", "4.2", "4.3"]},
            5: {"name": "Penalties and Driving Record", "subsections": ["5.1", "5.2"]},
            6: {"name": "License Types", "subsections": ["6.1", "6.2"]},
            7: {"name": "Other Important Information", "subsections": ["7.1"]}
        }
        
        # Create images directory if it doesn't exist
        self.images_dir = Path(__file__).parent / "images"
        self.images_dir.mkdir(exist_ok=True)
        
        # Load existing questions
        try:
            with open('questions.json', 'r') as f:
                self.current_questions = json.load(f)
            logging.info(f"Loaded {len(self.current_questions)} existing questions")
        except FileNotFoundError:
            self.current_questions = []
            logging.warning("No existing questions.json found")
        
        # Initialize Selenium with ChromeDriverManager
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--disable-gpu')  # Required for headless mode
        options.add_argument('--no-sandbox')  # Required for running as root
        options.add_argument('--disable-dev-shm-usage')  # Required for CI environments
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def download_image(self, img_url, section_num):
        """Download an image and save it to the images directory"""
        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                img_name = f"section_{section_num}_{Path(img_url).name}"
                img_path = self.images_dir / img_name
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                return img_name
        except Exception as e:
            logging.error(f"Failed to download image {img_url}: {str(e)}")
        return None

    def generate_gen_z_explanation(self, fact, category):
        """Generate a Gen Z style explanation"""
        templates = [
            "Bestie, listen up fr fr! {fact} That's just straight bussin' facts and you need to know this! ",
            "No cap, {fact} is giving main character energy! Skip this and you'll be catching Ls at the DMV! fr fr!",
            "The way {fact} just ate and left no crumbs? That's the kind of energy you need for the test fr fr!",
            "Ong this is crucial! {fact} Miss this and you'll be real quiet in the group chat after failing!",
            "Nah fr, {fact} is basic driving rizz! Don't be acting sus about this one bestie!",
            "It's giving responsible driver vibes! {fact} - that's just how we do it, no cap!",
            "This one's straight bussin'! {fact} Skip this and you'll get ratio'd by the examiner expeditiously!"
        ]
        return random.choice(templates).format(fact=fact)

    def scrape_subsection(self, section_num, subsection):
        """Scrape a specific subsection using Selenium"""
        url = f"{self.base_url}/{section_num}/subsection/{subsection}"
        logging.info(f"Scraping content from: {url}")
        
        try:
            self.driver.get(url)
            # Wait for content to load - try multiple selectors
            content = None
            selectors = [
                (By.CLASS_NAME, "manual-content"),
                (By.CLASS_NAME, "section-content"),
                (By.CLASS_NAME, "content"),
                (By.TAG_NAME, "article"),
                (By.TAG_NAME, "main"),
                (By.CLASS_NAME, "ng-star-inserted")  # Angular specific class
            ]
            
            for selector in selectors:
                try:
                    content = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(selector)
                    )
                    if content:
                        logging.info(f"Found content using selector: {selector}")
                        break
                except:
                    continue
            
            if not content:
                logging.error(f"Could not find content for section {section_num}.{subsection}")
                return []
            
            # Let the page fully render
            time.sleep(2)
            
            # Get images
            images = content.find_elements(By.TAG_NAME, "img")
            for img in images:
                img_url = img.get_attribute("src")
                if img_url:
                    img_name = self.download_image(img_url, section_num)
                    if img_name:
                        logging.info(f"Downloaded image: {img_name}")
            
            # Get text content - try multiple approaches
            text_elements = []
            for element_type in ["p", "div", "span"]:
                elements = content.find_elements(By.TAG_NAME, element_type)
                text_elements.extend([e for e in elements if e.text.strip()])
            
            questions = []
            current_text = ""
            
            for element in text_elements:
                text = element.text.strip()
                if text:
                    # Skip navigation text and other UI elements
                    if any(skip in text.lower() for skip in ["next", "previous", "back", "continue", "quiz"]):
                        continue
                        
                    # Combine short related paragraphs
                    if len(text) < 50:
                        current_text += " " + text
                    else:
                        if current_text:
                            questions.extend(self._create_questions(current_text, section_num))
                            current_text = ""
                        questions.extend(self._create_questions(text, section_num))
            
            # Handle any remaining text
            if current_text:
                questions.extend(self._create_questions(current_text, section_num))
            
            logging.info(f"Found {len(questions)} questions in section {section_num}.{subsection}")
            return questions
            
        except Exception as e:
            logging.error(f"Error scraping section {section_num}.{subsection}: {str(e)}")
            return []

    def _create_questions(self, text, section_num):
        """Helper method to create questions from text"""
        questions = []
        
        # Skip text that's too short or doesn't contain useful information
        if len(text) < 30 or not any(char.isalpha() for char in text):
            return questions
            
        # Create the question
        question = {
            "category": f"Section {section_num}: {self.sections[section_num]['name']}",
            "question": f"{text}?",
            "options": [
                "A. True",
                "B. False",
                "C. It depends on the situation",
                "D. Not required by law"
            ],
            "answer": "A",  # Default to True
            "explanation": self.generate_gen_z_explanation(text, self.sections[section_num]['name']),
            "image": None  # Will be updated if relevant image is found
        }
        questions.append(question)
        
        return questions

    def run(self):
        """Run the scraper for all sections"""
        all_questions = []
        
        try:
            for section_num, section_info in self.sections.items():
                logging.info(f"Scraping section {section_num}: {section_info['name']}")
                
                for subsection in section_info['subsections']:
                    logging.info(f"Scraping subsection {subsection}")
                    questions = self.scrape_subsection(section_num, subsection)
                    all_questions.extend(questions)
            
            # Combine with existing questions
            all_questions = self.current_questions + all_questions
            
            # Save to file
            with open('new_questions.json', 'w') as f:
                json.dump(all_questions, f, indent=4)
            
            logging.info(f"Saved {len(all_questions)} questions total")
            return True
            
        except Exception as e:
            logging.error(f"Error in main scraping process: {str(e)}")
            return False
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = DMVManualScraper(debug=True)
    success = scraper.run()
    
    if success:
        print("Ayy bestie, we just secured the bag with questions fr fr!")
        print("We got that knowledge straight from the DMV manual, it's giving main character energy!")
        print("Check new_questions.json for the bussin' results! No cap!")
    else:
        print("Bruh, we caught an L trying to scrape that content! Check the logs for the tea!")
