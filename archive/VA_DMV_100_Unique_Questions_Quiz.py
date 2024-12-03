from quiz_data import QuizData
import random

quiz = QuizData()

# IMAGE REQUIRED: Sign shape and symbol question
quiz.add_question(
    category="Road Signs",
    question="What does a yellow diamond-shaped sign with a deer indicate?",
    options=['Animal Crossing', 'Road Construction', 'Pedestrian Crossing', 'Stop'],
    correct_answer="Animal Crossing",
    response_correct={
        "text": "Yasss bestie! You're slaying this! ",
        "explanation": "That deer sign is giving 'watch out for animals' vibes fr fr!"
    },
    response_incorrect={
        "text": "Oof, not it bestie! ",
        "explanation": "The deer sign is all about animal crossings - no cap! Stay alert for our forest besties!"
    },
    image_path=".\\static\\dmv_images\\deer_crossing.jpg",
    image_alt="Deer crossing sign"
)

# IMAGE REQUIRED: Sign shape and symbol question
quiz.add_question(
    category="Road Signs",
    question="What does a circular yellow sign with two black 'R's indicate?",
    options=['Railroad Crossing', 'Stop Ahead', 'Speed Bump', 'Yield'],
    correct_answer="Railroad Crossing",
    response_correct={
        "text": "Period! You ate that! ",
        "explanation": "Those R's are giving choo-choo energy - railroad crossing ahead!"
    },
    response_incorrect={
        "text": "Not the vibe! ",
        "explanation": "Those R's are the railroad's way of saying 'watch out bestie!' - trains incoming!"
    },
    image_path=".\\static\\dmv_images\\railroad_crossing.jpg",
    image_alt="Railroad crossing sign"
)

# NO IMAGE NEEDED: General knowledge question about sign colors
quiz.add_question(
    category="Road Signs",
    question="What color are warning signs?",
    options=['Yellow', 'Red', 'Blue', 'Green'],
    correct_answer="Yellow",
    response_correct={
        "text": "Slay, bestie! You're on fire! ",
        "explanation": "Yellow signs are low-key warning you of potential dangers - stay alert!"
    },
    response_incorrect={
        "text": "Uh-uh, not quite! ",
        "explanation": "Yellow is the color of caution, bestie - warning signs are trying to tell you something!"
    },
    image_path=".\\static\\dmv_images\\yield.jpg",
    image_alt="Yellow warning sign"
)

# IMAGE REQUIRED: Traffic signal question
quiz.add_question(
    category="Rules of the Road",
    question="What does a flashing red traffic light mean?",
    options=['Stop and proceed when safe', 'Yield', 'Slow down', 'Keep driving'],
    correct_answer="Stop and proceed when safe",
    response_correct={
        "text": "Yaaas, you're a boss! ",
        "explanation": "Flashing red lights are like stop signs, bestie - come to a complete stop before moving on!"
    },
    response_incorrect={
        "text": "Not even close, bestie! ",
        "explanation": "Flashing red lights mean stop, then go when it's safe - don't get it twisted!"
    },
    image_path=".\\static\\dmv_images\\2redFlash.jpg",
    image_alt="Flashing red traffic light"
)

# IMAGE REQUIRED: Intersection scenario
quiz.add_question(
    category="Rules of the Road",
    question="When two vehicles arrive at an intersection at the same time, who has the right of way?",
    options=['The vehicle on the right', 'The larger vehicle', 'The vehicle on the left', 'Neither'],
    correct_answer="The vehicle on the right",
    response_correct={
        "text": "You're a genius, bestie! ",
        "explanation": "When in doubt, the vehicle on the right gets the right of way - it's just that simple!"
    },
    response_incorrect={
        "text": "Uh, nope! ",
        "explanation": "The vehicle on the right gets priority, bestie - don't get it backwards!"
    },
    image_path=".\\static\\dmv_images\\intersection.jpg",
    image_alt="Intersection with two vehicles"
)

# IMAGE REQUIRED: Road condition scenario
quiz.add_question(
    category="Safe Driving",
    question="What should you do when hydroplaning?",
    options=['Ease off the accelerator', 'Brake hard', 'Steer sharply', 'Speed up'],
    correct_answer="Ease off the accelerator",
    response_correct={
        "text": "You're a lifesaver, bestie! ",
        "explanation": "When hydroplaning, ease off the gas to regain traction - don't make it worse!"
    },
    response_incorrect={
        "text": "Not the move, bestie! ",
        "explanation": "Braking or steering sharply can make hydroplaning worse - ease off the accelerator instead!"
    },
    image_path=".\\static\\dmv_images\\hydroplaning.jpg",
    image_alt="Hydroplaning illustration"
)

# IMAGE REQUIRED: Night driving scenario
quiz.add_question(
    category="Safe Driving",
    question="When is it safest to use high beams?",
    options=['On open highways with no vehicles ahead', 'In the city', 'During fog', 'When following another car'],
    correct_answer="On open highways with no vehicles ahead",
    response_correct={
        "text": "You're a pro, bestie! ",
        "explanation": "High beams are perfect for open highways with no cars ahead - just don't blind anyone!"
    },
    response_incorrect={
        "text": "Not the safest choice, bestie! ",
        "explanation": "High beams can blind other drivers, so use them wisely - only on open highways with no cars ahead!"
    },
    image_path=".\\static\\dmv_images\\highBeams.jpg",
    image_alt="High beams illustration"
)

# NO IMAGE NEEDED: Legal consequence question
quiz.add_question(
    category="Penalties/Insurance",
    question="What is the consequence of driving with a suspended license?",
    options=['Fine and potential jail time', 'Community service', 'License renewal', 'No consequence'],
    correct_answer="Fine and potential jail time",
    response_correct={
        "text": "You're on point, bestie! ",
        "explanation": "Driving with a suspended license can lead to fines and even jail time - don't risk it!"
    },
    response_incorrect={
        "text": "Uh, no way! ",
        "explanation": "Driving with a suspended license is a big no-no - you could face fines and jail time!"
    },
    image_path=".\\static\\dmv_images\\suspendedLicense.jpg",
    image_alt="Suspended license illustration"
)

# NO IMAGE NEEDED: Insurance knowledge question
quiz.add_question(
    category="Penalties/Insurance",
    question="What does SR-22 insurance certify?",
    options=['Proof of financial responsibility', 'Lower insurance rates', 'Special privileges', 'License reinstatement'],
    correct_answer="Proof of financial responsibility",
    response_correct={
        "text": "You're a rockstar, bestie! ",
        "explanation": "SR-22 insurance proves you're financially responsible - it's a big deal!"
    },
    response_incorrect={
        "text": "Not quite, bestie! ",
        "explanation": "SR-22 insurance is all about proving financial responsibility - it's not about lower rates or special perks!"
    },
    image_path=".\\static\\dmv_images\\sr22Insurance.jpg",
    image_alt="SR-22 insurance illustration"
)

# NO IMAGE NEEDED: Legal consequence question
quiz.add_question(
    category="Alcohol/Drugs",
    question="What is the penalty for a first DUI offense in Virginia?",
    options=['$250 fine and license suspension', '$100 fine', 'No penalty', 'Warning'],
    correct_answer="$250 fine and license suspension",
    response_correct={
        "text": "You're a boss, bestie! ",
        "explanation": "A first DUI offense in Virginia can lead to a $250 fine and license suspension - don't drink and drive!"
    },
    response_incorrect={
        "text": "Uh, nope! ",
        "explanation": "A first DUI offense in Virginia comes with a $250 fine and license suspension - it's no joke!"
    },
    image_path=".\\static\\dmv_images\\duiPenalty.jpg",
    image_alt="DUI penalty illustration"
)

# IMAGE OPTIONAL: Could include vision impairment diagram
quiz.add_question(
    category="Alcohol/Drugs",
    question="How does alcohol affect vision?",
    options=['Reduces peripheral vision', 'Improves night vision', 'Increases reaction time', 'Has no effect'],
    correct_answer="Reduces peripheral vision",
    response_correct={
        "text": "You're on fire, bestie! ",
        "explanation": "Alcohol can reduce peripheral vision, making it harder to drive safely - stay sober!"
    },
    response_incorrect={
        "text": "Not even close, bestie! ",
        "explanation": "Alcohol can impair vision and reaction times - it's not worth the risk!"
    },
    image_path=".\\static\\dmv_images\\alcoholVision.jpg",
    image_alt="Alcohol vision illustration"
)

def get_random_questions(num_questions=35):
    """
    Get a random selection of questions following VA DMV test requirements:
    - Road Signs: 25% (9 questions)
    - Rules of the Road: 25% (9 questions)
    - Safe Driving: 20% (7 questions)
    - Penalties and Insurance: 15% (5 questions)
    - Alcohol and Drugs: 15% (5 questions)
    """
    all_questions = quiz.get_all_questions()
    
    # Group questions by category
    questions_by_category = {
        "Road Signs": [],
        "Rules of the Road": [],
        "Safe Driving": [],
        "Penalties/Insurance": [],
        "Alcohol/Drugs": []
    }
    
    for q in all_questions:
        category = q['category']
        if category in questions_by_category:
            questions_by_category[category].append(q)
    
    # Define number of questions needed from each category
    category_counts = {
        "Road Signs": 9,
        "Rules of the Road": 9,
        "Safe Driving": 7,
        "Penalties/Insurance": 5,
        "Alcohol/Drugs": 5
    }
    
    selected_questions = []
    used_questions = set()  # Track used questions to ensure uniqueness
    
    # Select questions from each category
    for category, count in category_counts.items():
        available_questions = [q for q in questions_by_category[category] 
                             if str(q) not in used_questions]  # Use string representation for set membership
        
        # If we don't have enough questions in this category, adjust other categories
        if len(available_questions) < count:
            print(f"Warning: Not enough questions in {category}. Only {len(available_questions)} available.")
            count = len(available_questions)
        
        # Randomly select questions from this category
        selected = random.sample(available_questions, count)
        selected_questions.extend(selected)
        
        # Add to used questions set
        for q in selected:
            used_questions.add(str(q))
    
    # If we somehow don't have enough questions (shouldn't happen with proper question bank)
    if len(selected_questions) < num_questions:
        remaining_needed = num_questions - len(selected_questions)
        print(f"Warning: Only got {len(selected_questions)} questions, needed {num_questions}")
        
        # Get all unused questions
        all_unused = [q for q in all_questions if str(q) not in used_questions]
        if all_unused:
            additional = random.sample(all_unused, min(remaining_needed, len(all_unused)))
            selected_questions.extend(additional)
    
    # Final shuffle of all selected questions
    random.shuffle(selected_questions)
    
    return selected_questions[:num_questions]

if __name__ == "__main__":
    # First print total questions per category
    all_questions = quiz.get_all_questions()
    total_counts = {}
    for q in all_questions:
        category = q['category']
        total_counts[category] = total_counts.get(category, 0) + 1
    
    print("\nTotal questions per category:")
    for category, count in total_counts.items():
        print(f"{category}: {count} questions")
    print(f"Total unique questions: {len(all_questions)}")
    
    # Now test random selection
    random_questions = get_random_questions(35)
    category_counts = {}
    for q in random_questions:
        category = q['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("\nRandom selection distribution:")
    for category, count in category_counts.items():
        print(f"{category}: {count} questions")
