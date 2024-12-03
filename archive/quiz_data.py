from typing import List, Dict, Optional
import json
import os

class QuizData:
    def __init__(self, data_dir: str = "./quiz_data"):
        self.questions: List[Dict] = []
        self.data_dir = data_dir
        # Use forward slashes
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        # Load questions from questions.json
        self.load_questions()

    def load_questions(self):
        """Load questions from questions.json"""
        try:
            with open('questions.json', 'r', encoding='utf-8') as f:
                questions = json.load(f)
                for q in questions:
                    # Convert to our format
                    self.questions.append({
                        'category': q.get('category', 'General Knowledge'),
                        'question': q.get('question', ''),
                        'options': q.get('options', []),
                        'correct_answer': q.get('answer', ''),
                        'explanation': q.get('explanation', ''),
                        'image': q.get('image', None)
                    })
        except Exception as e:
            print(f"Error loading questions: {e}")
            self.questions = []

    def add_question(self, 
                    category: str,
                    question: str,
                    options: List[str],
                    correct_answer: str,
                    response_correct: Dict[str, str] = None,  # GenZ responses for correct answer
                    response_incorrect: Dict[str, str] = None,  # GenZ responses for wrong answer
                    image_path: Optional[str] = None,
                    image_alt: Optional[str] = None):
        """Add a question to the quiz data
        
        Args:
            category: Question category (e.g., "Road Signs", "Traffic Laws")
            question: The question text
            options: List of possible answers
            correct_answer: The correct answer
            response_correct: Dict with GenZ-style correct response, e.g.,
                {"text": "Yasss! You nailed it! 💯", 
                 "explanation": "Stop signs are always octagonal and red - no cap!"}
            response_incorrect: Dict with GenZ-style incorrect response, e.g.,
                {"text": "Oof, not quite bestie! 😅",
                 "explanation": "The red octagonal sign means stop - fr fr!"}
            image_path: Path to image file (if any)
            image_alt: Alt text for accessibility
        """
        question_data = {
            "category": category,
            "question": question,
            "options": options,
            "correct_answer": correct_answer,
            "responses": {
                "correct": response_correct or {
                    "text": "Correct!",
                    "explanation": None
                },
                "incorrect": response_incorrect or {
                    "text": "Incorrect.",
                    "explanation": None
                }
            }
        }
        
        # Add image data if provided (using forward slashes)
        if image_path:
            question_data["image"] = {
                "path": image_path.replace("\\", "/"),
                "alt": image_alt or f"Image for question: {question[:30]}..."
            }
        
        self.questions.append(question_data)

    def save_to_json(self, filename: str = "quiz_questions.json"):
        """Save questions to JSON file using forward slashes"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, indent=2, ensure_ascii=False)

    def load_from_json(self, filename: str = "quiz_questions.json"):
        """Load questions from JSON file using forward slashes"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)

    def get_questions(self) -> List[Dict]:
        """Get all questions"""
        return self.questions

    def get_questions_by_category(self, category: str) -> List[Dict]:
        """Get questions filtered by category"""
        return [q for q in self.questions if q["category"] == category]

    def get_all_questions(self) -> List[Dict]:
        """Return all questions in the quiz."""
        return self.questions
