import json
import random
import os
import time
import sys

def load_questions():
    """Load questions from JSON file."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "questions.json")
        with open(json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: questions.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in questions.json")
        return []

def select_questions_by_category(questions, category, count):
    """Select specified number of questions from a category."""
    category_questions = [q for q in questions if q["category"] == category]
    if len(category_questions) < count:
        print(f"Warning: Only {len(category_questions)} questions available in {category} category.")
        return category_questions
    return random.sample(category_questions, count)

def administer_test(questions):
    """Present questions and collect answers."""
    total = len(questions)
    road_sign_total = sum(1 for q in questions if q["category"] == "Road Signs")
    
    print("\n=== Virginia DMV Knowledge Test ===")
    print(f"Total Questions: {total}")
    print(f"Road Signs: {road_sign_total} questions (requires 100% accuracy)")
    print(f"General Knowledge: {total - road_sign_total} questions (requires 80% accuracy)")
    print("=" * 40)
    
    input("\nPress Enter to begin...")

    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}/{total} - Category: {question['category']}")
        print(question["question"])
        print("-" * 40)
        
        for option in question["options"]:
            print(option)
            
        while True:
            answer = input("\nYour answer (A/B/C/D): ").strip().upper()
            if answer in ["A", "B", "C", "D"]:
                break
            print("Invalid input. Please enter A, B, C, or D.")
        
        question["user_answer"] = answer
        question["correct"] = answer == question["answer"]
        
        if question["correct"]:
            print("\n Correct!")
        else:
            print(f"\n Incorrect. The correct answer is {question['answer']}")
        
        print(f"Explanation: {question['explanation']}")
        input("\nPress Enter for next question...")

def review_incorrect(questions):
    """Review incorrect answers by category."""
    incorrect = [q for q in questions if not q["correct"]]
    if not incorrect:
        return
    
    print("\n=== Incorrect Answers Review ===")
    for q in incorrect:
        print(f"\nCategory: {q['category']}")
        print(q["question"])
        print("-" * 40)
        for option in q["options"]:
            print(option)
        print(f"\nYour answer: {q['user_answer']}")
        print(f"Correct answer: {q['answer']}")
        print(f"Explanation: {q['explanation']}")
        print("-" * 40)

def dramatic_print(text, delay=0.03):
    """Print text dramatically, character by character."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def dramatic_dots(count=3, delay=0.5):
    """Print dramatic dots."""
    for _ in range(count):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def display_dramatic_results(passed_signs, passed_general, road_sign_score, general_score, num_road_signs, num_general_knowledge):
    """Display results with dramatic effect."""
    print("\n" + "=" * 50)
    dramatic_print("Calculating final results", 0.05)
    dramatic_dots(4, 0.7)
    
    if passed_signs and passed_general:
        # Fake fail first
        dramatic_print("\nOh no... this isn't good...", 0.05)
        time.sleep(1)
        dramatic_print("I'm sorry, but you...", 0.05)
        time.sleep(1.5)
        
        # Clear several lines and show real result
        print("\n" * 5)
        dramatic_print("JUST KIDDING! ", 0.03)
        dramatic_print("CONGRATULATIONS! YOU PASSED THE TEST! ", 0.03)
        time.sleep(0.5)
        print("\nFinal Scores:")
        print(f"Road Signs: {road_sign_score}/{num_road_signs}")
        print(f"General Knowledge: {general_score}/{num_general_knowledge}")
        
    else:
        dramatic_print("\nCalculating how bad you failed...", 0.05)
        time.sleep(1)
        dramatic_print("DOUBLE FAIL! TRIPLE FAIL! QUADRUPLE FAIL!", 0.05)
        time.sleep(0.5)
        dramatic_print("YOU FAILED SO BAD YOU MADE HISTORY! ", 0.03)
        dramatic_print("MAYBE STICK TO RIDING THE BUS! ", 0.03)
        time.sleep(0.5)
        
        print("\nHere's how bad you did:")
        if not passed_signs:
            dramatic_print(f"Road Signs: {road_sign_score}/{num_road_signs} (Need 100% - EPIC FAIL! )", 0.03)
        if not passed_general:
            dramatic_print(f"General Knowledge: {general_score}/{num_general_knowledge} (Need 80% - MEGA FAIL! )", 0.03)
        
        dramatic_print("\nDon't worry, you can always try again... if you dare! ", 0.03)

def main():
    questions = load_questions()
    if not questions:
        return
    
    # Define test structure
    num_road_signs = 10
    num_general_knowledge = 25

    # Select and validate questions
    road_sign_questions = select_questions_by_category(questions, "Road Signs", num_road_signs)
    if len(road_sign_questions) < num_road_signs:
        print("Error: Insufficient road sign questions.")
        return

    general_questions = []
    for category in ["Traffic Laws", "Safe Driving", "Vehicle Control", "Special Conditions"]:
        category_questions = select_questions_by_category(questions, category, 
                                                        num_general_knowledge // 4)
        general_questions.extend(category_questions)

    if len(general_questions) < num_general_knowledge:
        print("Error: Insufficient general knowledge questions.")
        return

    # Combine and shuffle questions
    all_questions = road_sign_questions + general_questions[:num_general_knowledge]
    random.shuffle(all_questions)

    # Administer test
    administer_test(all_questions)
    
    # Calculate scores
    road_sign_score = sum(1 for q in road_sign_questions if q["correct"])
    general_score = sum(1 for q in general_questions if q["correct"])
    
    # Check pass/fail status
    passed_signs = road_sign_score == num_road_signs
    passed_general = general_score >= int(num_general_knowledge * 0.8)
    
    # Display dramatic results
    display_dramatic_results(passed_signs, passed_general, road_sign_score, general_score, 
                           num_road_signs, num_general_knowledge)
    
    if not (passed_signs and passed_general):
        if input("\nWant to see all the questions you messed up? (y/n): ").lower() == 'y':
            review_incorrect(all_questions)

if __name__ == "__main__":
    main()
