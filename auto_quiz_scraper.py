from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
import json
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quiz_scraper.log'),
        logging.StreamHandler()
    ]
)

class AutoQuizScraper:
    def __init__(self):
        self.base_url = "https://transactions.dmv.virginia.gov/dmv-manuals/#/sections/manual/1"
        self.output_file = Path('quiz_data.json')
        self.current_data = []

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
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
            print("\nCouldn't find element. Press Enter to show current page source, or 'q' to quit: ")
            user_input = input().lower()
            if user_input != 'q':
                print("\nCurrent page source:")
                print(driver.page_source)
                print("\nPress Enter to continue trying, or 'q' to quit: ")
                if input().lower() != 'q':
                    # Try one more time with longer timeout
                    try:
                        element = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((by, value))
                        )
                        return element
                    except:
                        return None
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
            print("\nCouldn't find elements. Press Enter to show current page source, or 'q' to quit: ")
            user_input = input().lower()
            if user_input != 'q':
                print("\nCurrent page source:")
                print(driver.page_source)
                print("\nPress Enter to continue trying, or 'q' to quit: ")
                if input().lower() != 'q':
                    # Try one more time with longer timeout
                    try:
                        elements = WebDriverWait(driver, 30).until(
                            EC.presence_of_all_elements_located((by, value))
                        )
                        return elements
                    except:
                        return []
            return []

    def wait_for_angular(self, driver, timeout=10):
        """Wait for Angular to finish rendering"""
        try:
            WebDriverWait(driver, timeout).until(
                lambda driver: driver.execute_script(
                    'return (window.angular !== undefined) && (angular.element(document).injector() !== undefined) && (angular.element(document).injector().get("$http").pendingRequests.length === 0)'
                )
            )
        except:
            logging.warning("Timeout waiting for Angular")

    def navigate_to_quiz(self, driver):
        """Navigate through the proper sequence to reach Section 2 quiz"""
        try:
            # Wait for Angular app to load
            self.wait_for_angular(driver)
            
            # Look for elements within the Angular view container
            view_container = self.wait_and_find_element(
                driver,
                By.CSS_SELECTOR,
                ".dmvNow-view-container [data-ui-view]"
            )
            if not view_container:
                logging.error("Could not find view container")
                return False

            # Wait for content to be present in view
            self.wait_for_angular(driver)
            
            # First find and click the section (looking for Section 2)
            section = self.wait_and_find_element(
                driver,
                By.XPATH,
                "//div[contains(@class, 'section-title') and contains(text(), 'Section 2')] | //h2[contains(text(), 'Section 2')] | //div[contains(@ng-click, 'section') and contains(text(), 'Section 2')]"
            )
            
            if section:
                section.click()
                logging.info("Clicked Section 2")
                # Wait for section content to load
                self.wait_for_angular(driver)
            else:
                logging.error("Could not find Section 2")
                return False

            # Now look for quiz button within the section
            quiz_button = self.wait_and_find_element(
                driver,
                By.CSS_SELECTOR,
                "[ng-click*='startQuiz'], [ng-click*='quiz'], button.quiz-button, .quiz-link"
            )
            
            if quiz_button:
                quiz_button.click()
                logging.info("Clicked Quiz button")
                self.wait_for_angular(driver)
                return True
            else:
                logging.error("Could not find quiz button")
                return False

        except Exception as e:
            logging.error(f"Error navigating to quiz: {str(e)}")
            print("\nError occurred. Current page source:")
            print(driver.page_source)
            return False

    def handle_question(self, driver):
        """Handle a single question, trying wrong answers first"""
        try:
            # Wait for Angular content
            self.wait_for_angular(driver)
            
            # Get the question text - look in Angular view
            question = self.wait_and_find_element(
                driver, 
                By.CSS_SELECTOR, 
                ".dmvNow-view-container [data-ui-view] .question, .dmvNow-view-container [data-ui-view] p.ng-binding"
            )
            if not question:
                print("\nCouldn't find question element. Press Enter to show current page source, or 'q' to quit: ")
                user_input = input().lower()
                if user_input != 'q':
                    print("\nCurrent page source:")
                    print(driver.page_source)
                return False

            question_text = question.text
            logging.info(f"\nQuestion: {question_text}")

            # Find all answer options
            options = self.wait_and_find_elements(
                driver,
                By.CSS_SELECTOR,
                ".dmvNow-view-container [data-ui-view] .answers button, .dmvNow-view-container [data-ui-view] [ng-click*='answer']"
            )
            
            if not options:
                return False

            # Store question data
            question_data = {
                'question': question_text,
                'options': [],
                'feedback': {}
            }

            # Try each option
            last_correct = None
            for opt in options:
                try:
                    option_text = opt.text.strip()
                    if not option_text:
                        continue

                    logging.info(f"Trying option: {option_text}")
                    opt.click()
                    time.sleep(1)

                    # Check for feedback
                    feedback = self.wait_and_find_element(
                        driver, 
                        By.XPATH, 
                        "//div[contains(@class, 'feedback')] | //p[contains(@class, 'feedback')]"
                    )
                    if feedback:
                        feedback_text = feedback.text
                        question_data['feedback'][option_text] = feedback_text
                        logging.info(f"Feedback: {feedback_text}")

                        # Check if this was correct (next question button appears)
                        next_button = self.wait_and_find_element(
                            driver, 
                            By.XPATH, 
                            "//button[contains(text(), 'Next')] | //span[contains(text(), 'Next')] | //div[contains(text(), 'Next')]"
                        )
                        if next_button:
                            last_correct = {
                                'text': option_text,
                                'feedback': feedback_text,
                                'element': next_button
                            }
                            break
                        else:
                            # Click try again to reset for next option
                            try_again = self.wait_and_find_element(
                                driver, 
                                By.XPATH, 
                                "//button[contains(text(), 'Try')] | //span[contains(text(), 'Try')] | //div[contains(text(), 'Try')]"
                            )
                            if try_again:
                                try_again.click()
                                time.sleep(1)

                except Exception as e:
                    logging.error(f"Error trying option: {str(e)}")
                    continue

            # Save question data
            self.current_data.append(question_data)
            self.save_data()

            # Move to next question if we found the correct answer
            if last_correct:
                last_correct['element'].click()
                time.sleep(1)
                return True

            return False

        except Exception as e:
            logging.error(f"Error handling question: {str(e)}")
            return False

    def save_data(self):
        """Save the current data to file"""
        try:
            with open(self.output_file, 'w') as f:
                json.dump(self.current_data, f, indent=2)
            logging.info("Data saved successfully")
        except Exception as e:
            logging.error(f"Error saving data: {str(e)}")

    def run_quiz(self):
        """Main method to run through the quiz automatically"""
        driver = self.setup_driver()
        try:
            # Load the main page and navigate to quiz
            driver.get(self.base_url)
            if not self.navigate_to_quiz(driver):
                logging.error("Failed to navigate to quiz")
                return

            logging.info("Quiz page loaded")

            # Handle each question
            while True:
                if not self.handle_question(driver):
                    break
                time.sleep(1)

        except Exception as e:
            logging.error(f"Error in quiz run: {str(e)}")
        finally:
            driver.quit()

def main():
    scraper = AutoQuizScraper()
    scraper.run_quiz()

if __name__ == "__main__":
    main()
