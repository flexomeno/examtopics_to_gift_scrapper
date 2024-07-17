from bs4 import BeautifulSoup
from datetime import datetime

def extract_questions_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    questions = []
    for question_div in soup.find_all('div', class_='question-body'):
        # Find the question number and text
        question_header = question_div.find('h5')
        question_description_div = question_div.find('div', class_='question-description option-text')
        if not question_header or not question_description_div:
            continue  # Skip this block if necessary elements are missing

        question_text = question_header.text.strip()
        question_description = question_description_div.text.strip()

        # Find the options
        options = []
        correct_answers = []
        for option in question_div.find_all('li'):
            option_text_div = option.find('div', class_='option-text')
            option_letter_div = option.find('div', class_='option-circle')
            if not option_text_div or not option_letter_div:
                continue  # Skip this option if necessary elements are missing

            option_text = option_text_div.text.strip()
            option_letter = option_letter_div.text.strip()
            is_correct = option.get('data-correct') == 'True'
            is_most_voted = option.find('div', class_='badge-voted badge-warning ui-selectee') is not None

            options.append(f"{option_letter}. {option_text}")
            if is_most_voted:
                correct_answers.append(option_letter)

        # Check for the fallback correct answer if no most voted
        if not correct_answers:
            correct_answer_span = question_div.find('span', class_='correct-answer')
            if correct_answer_span:
                correct_answers = [correct_answer_span.text.strip()]

        questions.append({
            'question': question_text,
            'description': question_description,
            'options': options,
            'correct_answers': correct_answers
        })
    
    return questions

def save_questions_to_file(questions, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for question in questions:
            file.write(f"Question {question['question']}:")
            file.write(f"{question['description']}\n")
            file.write("Answers:\n")
            for option in question['options']:
                file.write(f" - {option}\n")
            file.write(f"Correct Answer: {''.join(question['correct_answers'])}\n")
            file.write("========================================\n\n")

# Usage
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
file_path = 'secexams-SAA-C03/AWS Certified Solutions Architect - Associate SAA-C03 Exam - Free Exam Q&As, Page 30 _ SecExams.html'
output_file = f'extracted_questions_{timestamp}.txt'

questions = extract_questions_from_html(file_path)
save_questions_to_file(questions, output_file)

print(f"Questions have been saved to {output_file}")
