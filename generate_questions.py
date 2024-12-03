import json
import os
import random

def generate_road_sign_questions(num_questions=10):
    """Generate questions about road signs from section 2."""
    questions = []
    
    # Available signal images
    signal_images = {
        "green_arrow": ["2greenArrow.jpg", "2greenArrowdown.jpg"],
        "red_signals": ["2redLight.jpg", "2redArrow.jpg", "2redX.jpg", "2redFlash.jpg"],
        "yellow_signals": ["2yellowLight.jpg", "2yellowArrow.jpg", "2yellowArrow2.jpg", "2yellowFlash.jpg", "2yellowX.jpg"],
        "turn_signals": ["2leftTurnArrow1.jpg", "2leftTurnArrow2.jpg"]
    }
    
    # Question templates with associated images
    templates = [
        {
            "template": "What does this traffic signal indicate?",
            "image_category": "red_signals",
            "options": [
                "A. Stop and proceed when safe",
                "B. Complete stop required",
                "C. Slow down and proceed with caution",
                "D. Yield to oncoming traffic"
            ],
            "correct_answer": "B"
        },
        {
            "template": "When you see this signal, what should you do?",
            "image_category": "green_arrow",
            "options": [
                "A. Stop and wait",
                "B. Proceed with caution in the direction of the arrow",
                "C. Yield to pedestrians only",
                "D. Make a U-turn"
            ],
            "correct_answer": "B"
        },
        {
            "template": "This yellow signal means:",
            "image_category": "yellow_signals",
            "options": [
                "A. Speed up to clear the intersection",
                "B. Prepare to stop - the light is about to turn red",
                "C. Pedestrians have the right of way",
                "D. The intersection is closed"
            ],
            "correct_answer": "B"
        }
    ]
    
    for _ in range(num_questions):
        # Select a random template
        template = random.choice(templates)
        
        # Select a random image from the appropriate category
        image = random.choice(signal_images[template["image_category"]])
        
        question = {
            "category": "Road Signs",
            "question": template["template"],
            "options": template["options"],
            "image": image,
            "answer": template["correct_answer"],
            "explanation": create_explanation(template["image_category"])
        }
        questions.append(question)
    
    return questions

def generate_general_questions(num_questions=25):
    """Generate general knowledge questions."""
    questions = []
    
    # Available scenario images
    scenario_images = {
        "bus_safety": ["3busRoad1_v1.jpg", "3busRoad2_v1.jpg"],
        "hand_position": ["3handPosition_v1.jpg"],
        "safe_stopping": ["3safeStop.jpg"],
        "school_zone": ["schoolzonespeed.jpg"]
    }
    
    # Topics with associated images and answers
    topics = {
        "bus_safety": {
            "questions": [
                {
                    "text": "What should you do when approaching a school bus with flashing red lights?",
                    "options": [
                        "A. Pass quickly on the left",
                        "B. Pass quickly on the right",
                        "C. Stop until the bus moves or signals you to pass",
                        "D. Slow down but continue driving"
                    ],
                    "correct_answer": "C"
                },
                {
                    "text": "How far should you stay behind a school bus?",
                    "options": [
                        "A. 10 feet",
                        "B. 20 feet",
                        "C. 100 feet",
                        "D. 50 feet"
                    ],
                    "correct_answer": "C"
                }
            ],
            "images": scenario_images["bus_safety"]
        },
        "hand_position": {
            "questions": [
                {
                    "text": "What is the proper hand position on the steering wheel?",
                    "options": [
                        "A. 12 and 6 o'clock",
                        "B. 10 and 4 o'clock",
                        "C. 9 and 3 o'clock",
                        "D. 11 and 5 o'clock"
                    ],
                    "correct_answer": "C"
                }
            ],
            "images": scenario_images["hand_position"]
        },
        "safe_stopping": {
            "questions": [
                {
                    "text": "What is the proper way to come to a stop?",
                    "options": [
                        "A. Brake hard and fast",
                        "B. Pump the brakes rapidly",
                        "C. Apply steady pressure to the brake pedal",
                        "D. Use the emergency brake"
                    ],
                    "correct_answer": "C"
                }
            ],
            "images": scenario_images["safe_stopping"]
        }
    }
    
    for _ in range(num_questions):
        # Select a random topic
        topic = random.choice(list(topics.keys()))
        topic_data = topics[topic]
        
        # Select a random question from the topic
        question_data = random.choice(topic_data["questions"])
        
        # Create question
        question = {
            "category": "General Knowledge",
            "question": question_data["text"],
            "options": question_data["options"],
            "image": random.choice(topic_data["images"]) if topic_data["images"] else None,
            "answer": question_data["correct_answer"],
            "explanation": create_topic_explanation(topic)
        }
        questions.append(question)
    
    return questions

def create_explanation(topic):
    """Create an engaging explanation for the answer."""
    explanations = {
        "red_signals": "When you see a red signal, it means STOP! This isn't just a suggestion - it's a requirement for everyone's safety.",
        "green_arrow": "A green arrow means you can proceed in that direction, but always stay alert for pedestrians and other vehicles.",
        "yellow_signals": "Yellow means the light is about to turn red. Start slowing down and prepare to stop - don't try to beat the light!",
        "turn_signals": "These signals control turning movements. Always follow the direction indicated and yield to pedestrians."
    }
    return explanations.get(topic, "Safety first! Understanding traffic signals is crucial for everyone on the road.")

def create_topic_explanation(topic):
    """Create an explanation for a topic-based question."""
    explanations = {
        "bus_safety": "School buses carry our most precious cargo - children! Always be extra cautious around school buses and follow all signals.",
        "hand_position": "Proper hand position gives you the most control over your vehicle and helps prevent fatigue during long drives.",
        "safe_stopping": "Smooth, controlled stops are safer for you and your passengers, and they help prevent rear-end collisions."
    }
    return explanations.get(topic, "Understanding and following these rules keeps everyone safe on the road!")

def save_questions(questions):
    """Save generated questions to questions.json."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "questions.json")
    
    with open(output_file, "w") as f:
        json.dump(questions, f, indent=4)

def main():
    # Generate questions
    road_sign_questions = generate_road_sign_questions(10)  # 10 road sign questions
    general_questions = generate_general_questions(25)      # 25 general knowledge questions
    
    # Combine and shuffle questions
    all_questions = road_sign_questions + general_questions
    random.shuffle(all_questions)
    
    # Save questions
    save_questions(all_questions)
    print(f"Generated {len(all_questions)} questions and saved to questions.json")

if __name__ == "__main__":
    main()
