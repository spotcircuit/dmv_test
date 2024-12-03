# Importing Libraries
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, send_file
from io import BytesIO
import json
import random
import logging
from datetime import datetime, timedelta
import base64
import os

# Configure logging to a file
logging.basicConfig(
    filename='app_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Creating the Flask App
app = Flask(__name__, 
           static_url_path='/static',
           static_folder='static')
app.secret_key = 'dev'

# VA DMV test distribution
QUESTION_DISTRIBUTION = {
    'Road Signs': 9,
    'Traffic Signals': 5,
    'Rules of the Road': 7,
    'Safe Driving': 7,
    'Penalties and Insurance': 4,
    'Alcohol and Drugs': 3
}

# Load questions from JSON file
def load_questions():
    try:
        logging.info("Starting to load questions from new_questions.json")
        with open('new_questions.json', 'r', encoding='utf-8') as f:
            all_questions = json.load(f)
            logging.info(f"Loaded {len(all_questions)} questions from file")
            
            categories = {}
            app.questions_dict = {}
            
            for i, q in enumerate(all_questions):
                logging.info(f"Processing question {i}: {q.get('question', 'NO QUESTION FOUND')}")
                q['id'] = str(i)
                q['choices'] = q['options']
                app.questions_dict[str(i)] = q  # Add this line to store the question in the dictionary
                
                answer_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
                q['correct_index'] = answer_map.get(q['answer'], -1)  # Default to -1 if not found
                if q['correct_index'] == -1:
                    logging.warning(f"Invalid answer for question {i}: {q['answer']}")
                
                if 'image' in q and q['image'] and q['image'].strip():
                    q['image'] = f'dmv_images/{q["image"].strip()}'
                else:
                    q['image'] = None
                
                cat = q.get('category', 'General')
                logging.info(f"Question category: {cat}")
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(q)
            
            logging.info(f"Categories found: {list(categories.keys())}")
            logging.info(f"Question counts per category: {[(cat, len(qs)) for cat, qs in categories.items()]}")
            
            sections = []
            for category, count in QUESTION_DISTRIBUTION.items():
                logging.info(f"Processing category {category}, want {count} questions")
                if category in categories:
                    available = len(categories[category])
                    to_select = min(count, available)
                    logging.info(f"Found {available} questions in category {category}, selecting {to_select}")
                    questions = random.sample(categories[category], to_select)
                    sections.append({
                        'name': category,
                        'question_ids': [q['id'] for q in questions]
                    })
                    logging.info(f"Added {to_select} questions from {category}")
                else:
                    logging.warning(f"Category {category} not found in questions")
            
            if not sections:
                logging.error("No sections were created!")
                return None
                
            logging.info(f"Successfully loaded {sum(len(s['question_ids']) for s in sections)} questions across {len(sections)} sections")
            return sections
    except Exception as e:
        logging.error(f'Error loading questions: {str(e)}')
        return None

sections = load_questions()

def get_wrong_answer_roast(wrong_count):
    """Get progressively spicier roasts based on number of wrong answers"""
    roasts = {
        1: "Hmm... that's not it bestie. But we move! 💅",
        2: "The way you're getting these wrong... giving very much learner's permit energy 😩",
        3: "Three wrong? You're collecting L's like they're Pokemon cards bestie! 😭",
        4: "The DMV manual is not a choose-your-own-adventure book! 📚",
        5: "At this point, you're just guessing based on the vibes... and the vibes are OFF! 🤦‍♀️",
        6: "You're giving 'I only read the picture captions' energy rn... 👀",
        7: "The way you're failing... it's giving main character energy, but in a flop era 😔",
        8: "Bestie did you study this in your dreams? Because you're sleeping on these answers! 😴",
        9: "Your answers are more random than my Spotify shuffle! 🎵",
        10: "You're collecting wrong answers like they're limited edition! Make it stop! 😭",
        11: "The DMV test is not a TikTok challenge bestie... you can't just wing it! 📱",
        12: "Your test strategy is giving 'close my eyes and hope for the best' 👀",
        13: "The way you're missing these... it's giving 'I learned driving from GTA' energy 🎮",
        14: "Bestie, this is a DMV test, not a game of 'Wrong Answers Only'! 🚫",
        15: "Your wrong answers could fill a whole season of driving fails compilation! 📺"
    }
    # If they've got more wrong than our specific roasts, start cycling through random savage ones
    if wrong_count > 15:
        savage_roasts = [
            "At this point, just get a bus pass bestie... 🚌",
            "Your test performance is giving public transportation for life! 🚶‍♂️",
            "The way you're failing... uber drivers are breathing a sigh of relief! 🚗",
            "Walking is underrated anyway bestie! 👟",
            "Bicycle companies LOVE test takers like you! 🚲"
        ]
        return random.choice(savage_roasts)
    
    return roasts.get(wrong_count, "Oops! That's not correct!")

# Defining the Index Route
@app.route('/')
def index():
    global sections
    
    # If sections failed to load, try again
    if not sections:
        sections = load_questions()
        if not sections:
            return "Error: Failed to load questions. Check logs for details.", 500
    
    # Initialize session if needed
    if 'current_section' not in session:
        session['current_section'] = 0
        session['current_question'] = 0
        session['sections'] = sections
        session['score'] = 0
        session['wrong_count'] = 0
        session.modified = True
    
    logging.debug(f"Sections loaded: {sections}")
    logging.debug(f"Session data: {session.items()}")
    
    current_section_idx = session['current_section']
    current_question_idx = session['current_question']
    
    logging.debug(f"Current section index: {current_section_idx}, Total sections: {len(sections)}")
    logging.debug(f"Current question index: {current_question_idx}, Total questions in current section: {len(sections[current_section_idx]['question_ids'])}")
    
    if current_section_idx >= len(sections):
        return redirect(url_for('results'))
        
    current_section = sections[current_section_idx]
    question_id = current_section['question_ids'][current_question_idx]
    
    try:
        question = app.questions_dict[question_id]
    except KeyError:
        logging.warning(f"Invalid question ID: {question_id}")
        return redirect(url_for('results'))
    
    return render_template('test.html',
                         question=question['question'],
                         choices=question['choices'],
                         image_path=question.get('image', ''))

# Defining the Submit Answer Route
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    selected_answer = int(data['selected_answer'])
    
    current_section = session['current_section']
    current_question = session['current_question']
    
    if current_section >= len(sections):
        return jsonify({'quiz_complete': True})
        
    question_id = sections[current_section]['question_ids'][current_question]
    question = app.questions_dict[question_id]
    
    is_correct = selected_answer == question['correct_index']
    
    if is_correct:
        session['score'] += 1
        # Only advance to next question if answer is correct
        session['current_question'] += 1
        if session['current_question'] >= len(sections[current_section]['question_ids']):
            session['current_section'] += 1
            session['current_question'] = 0
    else:
        session['wrong_count'] += 1
    
    session.modified = True
    
    quiz_complete = session['current_section'] >= len(sections)
    
    return jsonify({
        'correct': is_correct,
        'explanation': question.get('explanation', 'No explanation available'),
        'quiz_complete': quiz_complete
    })

# Defining the Results Route
@app.route('/results')
def results():
    if 'current_section' not in session:
        return redirect(url_for('index'))
    
    correct_count = session.get('score', 0)
    wrong_count = session.get('wrong_count', 0)
    total_questions = sum(len(section['question_ids']) for section in sections)
    passed = correct_count >= 30  # Need at least 30 out of 35 correct to pass
    
    # Final results roast based on overall performance
    if passed:
        if correct_count == 35:
            message = "PERIODT! YOU DEVOURED THIS TEST AND LEFT NO CRUMBS! 💅✨ DMV QUEEN/KING BEHAVIOR!"
        elif correct_count >= 33:
            message = "THE SERVE! Almost perfect bestie, you really ate that! 💃✨"
        else:
            message = "You passed! Not the most glamorous performance, but we take those! 💁‍♀️✨"
    else:
        if wrong_count >= 25:
            message = (
                "The way you failed... it's actually impressive? 😭 "
                "Like you had to TRY to get this many wrong! "
                "See you in 15 days after you actually READ the manual! 📚"
            )
        elif wrong_count >= 15:
            message = (
                "Bestie... your performance is giving 'I learned driving from Mario Kart'! 🎮 "
                "The DMV said 'Thank u, next!' Try again in 15 days! 😩"
            )
        else:
            message = (
                f"SO CLOSE YET SO FAR! Only needed {30 - correct_count} more right! "
                "You're giving 'almost ate' but the DMV said 'still hungry'! "
                "Come back in 15 days bestie! 😔✨"
            )
    
    return render_template('results.html',
                         passed=passed,
                         message=message,
                         correct_count=correct_count,
                         wrong_count=wrong_count,
                         total_questions=total_questions)

# Defining the Regenerate Route
@app.route('/regenerate')
def regenerate():
    session.clear()
    return redirect(url_for('index'))

# Running the App
if __name__ == '__main__':
    app.run(port=3022, debug=True)
