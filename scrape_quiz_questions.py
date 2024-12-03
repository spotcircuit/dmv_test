from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import time
import json
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quiz_observer.log'),
        logging.StreamHandler()
    ]
)

class DMVQuizScraper:
    def __init__(self):
        self.base_url = "https://transactions.dmv.virginia.gov/dmv-manuals/#/sections/manual/1"
        self.output_file = Path('quiz_data.json')
        self.current_data = []

    def setup_driver(self):
        chrome_options = Options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        return driver

    def wait_and_find_element(self, driver, by, value, timeout=10):
        """Wait for element to be present and return it"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logging.error(f"Timeout waiting for element: {value}")
            return None

    def wait_and_find_elements(self, driver, by, value, timeout=10):
        """Wait for elements to be present and return them"""
        try:
            elements = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except TimeoutException:
            logging.error(f"Timeout waiting for elements: {value}")
            return []

    def record_quiz_state(self, driver):
        """Record the current state of the quiz"""
        try:
            # Get question text
            question_elem = self.wait_and_find_element(driver, By.CLASS_NAME, "question-text")
            if question_elem:
                question_text = question_elem.text
                logging.info(f"\nQuestion found: {question_text}")

                # Get all options
                options = self.wait_and_find_elements(driver, By.CLASS_NAME, "option-text")
                options_text = [opt.text for opt in options]
                logging.info(f"Options found: {options_text}")

                # Get any images
                images = driver.find_elements(By.TAG_NAME, "img")
                image_data = []
                for img in images:
                    try:
                        src = img.get_attribute("src")
                        alt = img.get_attribute("alt")
                        if src and alt:
                            image_data.append({"src": src, "alt": alt})
                            logging.info(f"Image found - src: {src}, alt: {alt}")
                    except:
                        continue

                # Save the current state
                state = {
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'question': question_text,
                    'options': options_text,
                    'images': image_data
                }

                self.current_data.append(state)
                self.save_data()

        except Exception as e:
            logging.error(f"Error recording quiz state: {str(e)}")

    def record_feedback(self, driver):
        """Record feedback after an answer"""
        try:
            feedback_elem = self.wait_and_find_element(driver, By.CLASS_NAME, "feedback-text")
            if feedback_elem:
                feedback_text = feedback_elem.text
                logging.info(f"Feedback found: {feedback_text}")

                # Update the last recorded state with feedback
                if self.current_data:
                    self.current_data[-1]['feedback'] = feedback_text
                    self.save_data()

        except Exception as e:
            logging.error(f"Error recording feedback: {str(e)}")

    def save_data(self):
        """Save the current data to file"""
        try:
            with open(self.output_file, 'w') as f:
                json.dump(self.current_data, f, indent=2)
            logging.info("Data saved successfully")
        except Exception as e:
            logging.error(f"Error saving data: {str(e)}")

    def observe_quiz(self):
        """Main method to observe the quiz"""
        driver = self.setup_driver()
        try:
            # Load the page
            driver.get(self.base_url)
            time.sleep(5)  # Wait for Angular
            logging.info("Page loaded")

            while True:
                try:
                    # Wait for user input
                    user_input = input("\nPress Enter to record current state (or 'q' to quit): ").lower()
                    if user_input == 'q':
                        break

                    # Record current state
                    self.record_quiz_state(driver)
                    
                    # Wait for feedback input
                    user_input = input("\nPress Enter after selecting an answer to record feedback (or 'q' to quit): ").lower()
                    if user_input == 'q':
                        break
                    
                    # Record feedback if present
                    self.record_feedback(driver)
                except EOFError:
                    logging.info("Input stream ended. Exiting...")
                    break
                except KeyboardInterrupt:
                    logging.info("User interrupted. Exiting...")
                    break

        except Exception as e:
            logging.error(f"Error in quiz observation: {str(e)}")
        finally:
            driver.quit()

def main():
    scraper = DMVQuizScraper()
    scraper.observe_quiz()

if __name__ == "__main__":
    main()
