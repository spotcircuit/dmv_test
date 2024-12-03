import json
from difflib import SequenceMatcher
import itertools

def similar(a, b, threshold=0.8):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold

def check_duplicates():
    # Load questions
    with open('new_questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"\nTotal questions: {len(questions)}\n")
    
    # Check for exact duplicates
    seen_questions = {}
    exact_duplicates = []
    
    for i, q in enumerate(questions):
        question_text = q['question'].strip().lower()
        if question_text in seen_questions:
            exact_duplicates.append((i, seen_questions[question_text], q))
        else:
            seen_questions[question_text] = i
    
    # Print exact duplicates
    if exact_duplicates:
        print("=== EXACT DUPLICATES FOUND ===")
        for i, orig_idx, q in exact_duplicates:
            print(f"\nDuplicate at index {i} matches index {orig_idx}")
            print(f"Question: {q['question']}")
            print(f"Category: {q['category']}")
            print("-" * 50)
    else:
        print("No exact duplicates found.")
    
    # Check for similar questions
    print("\n=== CHECKING FOR SIMILAR QUESTIONS ===")
    similar_pairs = []
    
    for i, j in itertools.combinations(range(len(questions)), 2):
        q1, q2 = questions[i], questions[j]
        if similar(q1['question'], q2['question']):
            similar_pairs.append((i, j, q1, q2))
    
    # Print similar questions
    if similar_pairs:
        print("\nPotentially similar questions found:")
        for i, j, q1, q2 in similar_pairs:
            similarity = SequenceMatcher(None, q1['question'].lower(), q2['question'].lower()).ratio()
            print(f"\nSimilarity: {similarity:.2%}")
            print(f"Index {i}: [{q1['category']}] {q1['question']}")
            print(f"Index {j}: [{q2['category']}] {q2['question']}")
            print("-" * 50)
    else:
        print("No similar questions found.")

if __name__ == "__main__":
    check_duplicates()
