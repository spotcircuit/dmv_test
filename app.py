# Importing Libraries
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, send_file, send_from_directory
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

# Mode constants
PRACTICE_MODE = 'practice'
TEST_MODE = 'test'

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

# Initialize sections with fallback
sections = load_questions() or []  

# Defining the Index Route
@app.route('/')
def index():
    return redirect(url_for('select_mode'))

# Defining the Test Route
@app.route('/test')
def test():
    if 'mode' not in session:
        return redirect(url_for('select_mode'))
    
    # Get current position
    current_section = session.get('current_section', 0)
    current_question = session.get('current_question', 0)
    
    # Check if we're done
    if current_section >= len(sections):
        return redirect(url_for('results'))
    
    # Get current question
    question_id = sections[current_section]['question_ids'][current_question]
    question = app.questions_dict[question_id]
    
    # Prepare progress data
    progress = {
        'current': session.get('total_answered', 0),
        'total': sum(len(section['question_ids']) for section in sections),
        'correct': session.get('score', 0),
        'wrong': session.get('wrong_count', 0),
        'streak': session.get('streak', 0),
        'max_streak': session.get('max_streak', 0)
    }
    
    return render_template('test.html',
                         question=question['question'],
                         choices=question['choices'],
                         image_path=question.get('image', ''),
                         mode=session['mode'],
                         progress=progress)

@app.route('/select_mode')
def select_mode():
    # Clear mode from session to ensure fresh start
    session.clear()
    return render_template('select_mode.html')

@app.route('/set_mode/<mode>')
def set_mode(mode):
    if mode not in [PRACTICE_MODE, TEST_MODE]:
        return redirect(url_for('select_mode'))
    
    # Set mode in session
    session['mode'] = mode
    
    # Initialize sections if needed
    global sections
    if not sections:
        sections = load_questions() or []
    
    return redirect(url_for('test'))

@app.route('/reload_questions')
def reload_questions():
    # Keep only the mode
    current_mode = session.get('mode', PRACTICE_MODE)
    session.clear()
    session['mode'] = current_mode
    
    # Force questions to reload
    global sections
    sections = load_questions()
    if sections is None:  # If loading failed
        return "Error: Failed to load questions. Check logs for details.", 500
    
    return redirect(url_for('test'))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'mode' not in session:
        return jsonify({
            'error': 'No mode selected'
        }), 400

    data = request.get_json()
    if not data or 'selected_answer' not in data:
        return jsonify({
            'error': 'No answer provided'
        }), 400

    selected_answer = int(data['selected_answer'])
    current_section = session.get('current_section', 0)
    current_question = session.get('current_question', 0)

    # Get current question
    question_id = sections[current_section]['question_ids'][current_question]
    question = app.questions_dict[question_id]
    correct_answer = question['correct_index']  
    
    # Check if answer is correct
    is_correct = selected_answer == correct_answer
    
    # Update session stats
    session['total_answered'] = session.get('total_answered', 0) + 1
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
        session['streak'] = session.get('streak', 0) + 1
        session['max_streak'] = max(session.get('max_streak', 0), session['streak'])
    else:
        session['wrong_count'] = session.get('wrong_count', 0) + 1
        session['streak'] = 0
    
    # In test mode, always move to next question
    # In practice mode, only move on if correct
    should_advance = session['mode'] == TEST_MODE or is_correct
    
    if should_advance:
        # Move to next question
        current_question += 1
        if current_question >= len(sections[current_section]['question_ids']):
            current_section += 1
            current_question = 0
        
        session['current_section'] = current_section
        session['current_question'] = current_question
    
    # Check if quiz is complete
    quiz_complete = current_section >= len(sections)
    
    return jsonify({
        'correct': is_correct,
        'explanation': question.get('explanation', ''),
        'quiz_complete': quiz_complete
    })

# Serve static images
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    try:
        return send_from_directory('static/images', filename)
    except Exception as e:
        logging.error(f'Error serving image {filename}: {str(e)}')
        return '', 404  # Return empty response if image not found

# Defining the Results Route
@app.route('/results')
def results():
    if 'current_section' not in session:
        return redirect(url_for('test'))
    
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
    return redirect(url_for('test'))

# Running the App
if __name__ == '__main__':
    app.run(port=3022, debug=True)
