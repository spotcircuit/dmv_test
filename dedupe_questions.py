import json

# Load questions
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Create a set to track seen questions
seen_questions = set()
unique_questions = []

# Filter out duplicates while preserving order
for question in questions:
    q_text = question['question']
    if q_text not in seen_questions:
        seen_questions.add(q_text)
        unique_questions.append(question)

print(f"Original questions: {len(questions)}")
print(f"Unique questions: {len(unique_questions)}")

# Save the deduplicated questions
with open('questions.json', 'w') as f:
    json.dump(unique_questions, f, indent=4)
