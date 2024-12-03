import json

def clean_questions():
    # Load questions
    with open('new_questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Original question count: {len(questions)}")
    
    # Create backup of original
    with open('new_questions_backup.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)
    
    # Find and remove duplicates based on question text
    duplicates = []
    
    # Hospital sign questions
    hospital_questions = [(i, q) for i, q in enumerate(questions) 
                         if 'H' in q['question'] and 'blue' in q['question'].lower()]
    if len(hospital_questions) > 1:
        # Keep the first one, mark others for removal
        duplicates.extend([i for i, _ in hospital_questions[1:]])
    
    # Brake failure questions
    brake_questions = [(i, q) for i, q in enumerate(questions) 
                      if 'brake' in q['question'].lower() and 'fail' in q['question'].lower()]
    if len(brake_questions) > 1:
        # Keep the more specific one (usually longer)
        sorted_brake = sorted(brake_questions, key=lambda x: len(x[1]['question']), reverse=True)
        duplicates.extend([i for i, _ in sorted_brake[1:]])
    
    # Fog driving questions
    fog_questions = [(i, q) for i, q in enumerate(questions) 
                    if 'fog' in q['question'].lower() and 'driving' in q['question'].lower()]
    if len(fog_questions) > 1:
        # Keep the more specific one
        sorted_fog = sorted(fog_questions, key=lambda x: len(x[1]['question']), reverse=True)
        duplicates.extend([i for i, _ in sorted_fog[1:]])
    
    # BAC questions - check for duplicates while preserving age-specific ones
    bac_questions = [(i, q) for i, q in enumerate(questions) 
                    if 'BAC' in q['question'] or 'blood alcohol' in q['question'].lower()]
    for i, q1 in bac_questions:
        for j, q2 in bac_questions:
            if i < j and ('21' in q1['question']) == ('21' in q2['question']):
                duplicates.append(j)
    
    # Remove duplicates
    cleaned_questions = [q for i, q in enumerate(questions) if i not in duplicates]
    
    print(f"Questions removed: {len(duplicates)}")
    print(f"New question count: {len(cleaned_questions)}")
    print("\nDuplicates removed:")
    for i in duplicates:
        print(f"- {questions[i]['question']}")
    
    # Save cleaned questions
    with open('new_questions.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_questions, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    clean_questions()
