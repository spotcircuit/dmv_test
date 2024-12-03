import pdfplumber
import json
import re
from pathlib import Path
import logging
import random
import requests
import os
from PIL import Image
import io

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_parser.log'),
        logging.StreamHandler()
    ]
)

class DMVManualParser:
    def __init__(self, pdf_path, debug=False):
        self.pdf_path = pdf_path
        self.debug = debug
        self.sections = {}
        self.current_questions = []
        self.image_counter = 1
        
        # Create dmv_images directory if it doesn't exist
        self.images_dir = Path('static/dmv_images')
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing questions
        try:
            with open('questions.json', 'r') as f:
                self.current_questions = json.load(f)
            logging.info(f"Loaded {len(self.current_questions)} existing questions")
        except FileNotFoundError:
            logging.warning("No existing questions.json found")

    def extract_images(self, page):
        """Extract images from a PDF page"""
        try:
            for image in page.images:
                # Generate a unique filename
                image_type = image['stream'].get('/Subtype', '').lower()
                if image_type == '/image':
                    ext = self.get_image_extension(image)
                    if not ext:
                        continue
                        
                    filename = f"{self.image_counter}{ext}"
                    image_path = self.images_dir / filename
                    
                    # Save the image
                    image_data = image['stream'].get_data()
                    img = Image.open(io.BytesIO(image_data))
                    img.save(image_path)
                    
                    logging.info(f"Saved image: {filename}")
                    self.image_counter += 1
                    return filename
        except Exception as e:
            logging.error(f"Error extracting image: {str(e)}")
        return None

    def get_image_extension(self, image):
        """Determine the image file extension based on the stream filter"""
        filter_type = image['stream'].get('/Filter', '')
        if isinstance(filter_type, list):
            filter_type = filter_type[0]
        
        filter_map = {
            '/DCTDecode': '.jpg',
            '/JPXDecode': '.jp2',
            '/FlateDecode': '.png'
        }
        
        return filter_map.get(filter_type, '.jpg')

    def extract_text(self):
        """Extract text and images from PDF with section markers"""
        logging.info(f"Starting PDF extraction from {self.pdf_path}")
        all_text = ""
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    # Extract images first
                    image_filename = self.extract_images(page)
                    
                    # Extract text
                    text = page.extract_text()
                    if self.debug:
                        logging.debug(f"Extracted page text: {text[:200]}...")
                    all_text += text + "\n"
                    
                    # If we found an image, associate it with the nearest question
                    if image_filename and self.current_questions:
                        # Find the last question that doesn't have an image
                        for question in reversed(self.current_questions):
                            if 'image' not in question or not question['image']:
                                question['image'] = image_filename
                                break
                    
            logging.info("PDF extraction completed successfully")
            return all_text
        except Exception as e:
            logging.error(f"Error extracting PDF: {str(e)}")
            return None

    def parse_sections(self, text):
        """Parse text into sections based on headers"""
        # Common section markers in DMV manuals
        section_patterns = [
            r'Section \d+[:.]\s*([^\n]+)',
            r'Chapter \d+[:.]\s*([^\n]+)',
            r'\d+\.\s+([A-Z][^\n]+)'
        ]
        
        current_section = "General"
        current_text = []
        
        for line in text.split('\n'):
            # Check if line starts a new section
            for pattern in section_patterns:
                if re.match(pattern, line):
                    if current_text:
                        self.sections[current_section] = '\n'.join(current_text)
                    current_section = line
                    current_text = []
                    break
            current_text.append(line)
            
        # Add the last section
        if current_text:
            self.sections[current_section] = '\n'.join(current_text)
            
        if self.debug:
            logging.debug(f"Found sections: {list(self.sections.keys())}")
            
        return self.sections

    def generate_question(self, text_chunk):
        """Generate a question from a chunk of text"""
        # Simple rule-based question generation
        # Look for sentences with key terms that might make good questions
        key_terms = [
            "must", "should", "required", "illegal", "law", "regulation",
            "speed limit", "signal", "sign", "right of way", "penalty"
        ]
        
        sentences = text_chunk.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if any(term in sentence.lower() for term in key_terms):
                # Create a question
                question = {
                    "category": "General Knowledge",
                    "question": f"{sentence}?",
                    "options": [
                        "A. True",
                        "B. False",
                        "C. It depends on the situation",
                        "D. None of the above"
                    ],
                    "answer": "A",  # Default to True for now
                    "explanation": self.generate_gen_z_explanation(sentence)
                }
                return question
        return None

    def generate_gen_z_explanation(self, fact):
        """Generate a Gen Z style explanation"""
        templates = [
            "Fr fr, {fact} - that's just straight bussin' facts! No cap, ignore this and you'll be catching Ls! 💀",
            "Bestie, listen up! {fact} is giving main character energy! Skip this and you'll be real quiet in the group chat! 😤",
            "Ong this is important! {fact} ain't just for the aesthetic, it's literally how you avoid becoming a whole flop era! 🚫",
            "No shade but {fact} is basic driving rizz! Miss this and you'll be posting your L's on BeReal fr fr! 💅",
            "It's giving safety vibes! {fact} - ignore this and you'll be ratio'd by the driving examiner expeditiously! 😭"
        ]
        return random.choice(templates).format(fact=fact)

    def process_manual(self):
        """Main processing function"""
        logging.info("Starting manual processing")
        
        # Extract text
        text = self.extract_text()
        if not text:
            return False
            
        # Parse sections
        sections = self.parse_sections(text)
        
        # Generate questions
        new_questions = []
        for section, content in sections.items():
            if self.debug:
                logging.debug(f"Processing section: {section}")
            
            # Split content into manageable chunks
            chunks = content.split('\n\n')
            for chunk in chunks:
                question = self.generate_question(chunk)
                if question:
                    new_questions.append(question)
                    
        # Combine with existing questions
        all_questions = self.current_questions + new_questions
        
        # Save to file
        with open('new_questions.json', 'w') as f:
            json.dump(all_questions, f, indent=4)
            
        logging.info(f"Generated {len(new_questions)} new questions")
        return True

def download_manual():
    """Download the Virginia Driver's Manual PDF"""
    url = "https://www.dmv.virginia.gov/webdoc/pdf/dmv39.pdf"
    pdf_path = Path(__file__).parent / "dmv39.pdf"
    
    if not pdf_path.exists():
        logging.info("Downloading Virginia Driver's Manual PDF...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            logging.info(f"Downloaded manual to {pdf_path}")
            return pdf_path
        else:
            logging.error("Failed to download manual")
            return None
    return pdf_path

if __name__ == "__main__":
    # Download the manual if needed
    pdf_path = download_manual()
    if pdf_path:
        parser = DMVManualParser(pdf_path, debug=True)
        success = parser.process_manual()
        if success:
            print("✨ Ayy, we just parsed that manual fr fr! Check new_questions.json for the bussin' results! No cap! 🔥")
        else:
            print("💀 Bruh, we caught an L trying to parse that PDF! Check the logs for the tea! ☕")
    else:
        logging.error("Could not proceed without manual PDF")
