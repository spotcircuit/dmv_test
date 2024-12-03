import json

def clean_questions():
    # Load questions
    with open('new_questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Original question count: {len(questions)}")
    
    # Keep track of questions to remove
    to_remove = set()
    
    # Hospital sign questions (merge 8 and 16)
    # Keep the more descriptive version
    to_remove.add(16)
    
    # Brake failure questions (merge 24 and 79)
    # Keep the more specific version
    to_remove.add(24)
    
    # Fog driving questions (merge 45 and 67)
    # Keep the more specific version
    to_remove.add(45)
    
    # Create new question list without duplicates
    cleaned_questions = [q for i, q in enumerate(questions) if i not in to_remove]
    
    print(f"Questions removed: {len(to_remove)}")
    print(f"New question count: {len(cleaned_questions)}")
    
    # Save cleaned questions
    with open('new_questions.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_questions, f, indent=4, ensure_ascii=False)
    
    # Create backup of original
    with open('new_questions_backup.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    clean_questions()
