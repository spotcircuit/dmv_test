import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    """Setup Chrome driver with options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_sample_questions(driver, num_samples=5):
    """Extract sample questions from DMV practice tests."""
    # Virginia DMV practice test URL
    url = "https://www.dmv.virginia.gov/drivers/#quiz.asp"
    driver.get(url)
    
    # Wait for quiz to load
    wait = WebDriverWait(driver, 10)
    questions = []
    
    try:
        # Navigate through questions
        for _ in range(num_samples):
            # Wait for question to load
            question_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".question-text")))
            
            # Get question details
            question_text = question_elem.text
            
            # Check for images
            images = driver.find_elements(By.CSS_SELECTOR, ".question-image img")
            image_urls = [img.get_attribute("src") for img in images]
            
            # Get options
            options = driver.find_elements(By.CSS_SELECTOR, ".answer-option")
            options_text = [opt.text for opt in options]
            
            question_data = {
                "question": question_text,
                "options": options_text,
                "has_image": len(image_urls) > 0,
                "image_urls": image_urls
            }
            questions.append(question_data)
            
            # Click next if available
            next_button = driver.find_element(By.CSS_SELECTOR, ".next-button")
            if next_button.is_enabled():
                next_button.click()
                time.sleep(1)  # Small delay for next question to load
            
    except Exception as e:
        print(f"Error extracting questions: {str(e)}")
    
    return questions

def analyze_question_patterns(questions):
    """Analyze patterns in DMV questions."""
    patterns = {
        "total_questions": len(questions),
        "questions_with_images": sum(1 for q in questions if q["has_image"]),
        "avg_options": sum(len(q["options"]) for q in questions) / len(questions),
        "common_phrases": [],
        "image_patterns": []
    }
    
    # Analyze question patterns
    for q in questions:
        # Look for common question starters
        words = q["question"].lower().split()
        if len(words) > 2:
            patterns["common_phrases"].append(" ".join(words[:2]))
        
        # Analyze image patterns if present
        if q["has_image"]:
            patterns["image_patterns"].append({
                "question_type": "sign" if "sign" in q["question"].lower() else "scenario",
                "image_count": len(q["image_urls"])
            })
    
    return patterns

def save_analysis(questions, patterns):
    """Save the sample questions and analysis."""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Save sample questions
    with open(os.path.join(output_dir, "sample_questions.json"), "w") as f:
        json.dump(questions, f, indent=4)
    
    # Save analysis
    with open(os.path.join(output_dir, "question_analysis.json"), "w") as f:
        json.dump(patterns, f, indent=4)

def main():
    print("Starting DMV question analysis...")
    driver = setup_driver()
    
    try:
        # Extract sample questions
        questions = extract_sample_questions(driver)
        print(f"Extracted {len(questions)} sample questions")
        
        # Analyze patterns
        patterns = analyze_question_patterns(questions)
        print("\nAnalysis Results:")
        print(f"Total Questions: {patterns['total_questions']}")
        print(f"Questions with Images: {patterns['questions_with_images']}")
        print(f"Average Options per Question: {patterns['avg_options']:.1f}")
        
        # Save results
        save_analysis(questions, patterns)
        print("\nResults saved to sample_questions.json and question_analysis.json")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
