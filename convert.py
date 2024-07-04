import re
import os
import openai

# Configuración de la API de OpenAI
openai.api_key = os.getenv("openapikey")

# Función para solicitar la justificación de la respuesta correcta a ChatGPT
def get_feedback(question, correct_answer, wrong_answers):
    prompt = f"Explain why the answer is '{correct_answer}' and not these answers: '{wrong_answers}' for the following question in less than 160 words: {question}. Also list services which appear in all answers and give a very brief description."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AWS expert"},
            {"role": "user", "content": prompt}
        ]
    )
    feedback = response['choices'][0]['message']['content']
    # Reemplazar dobles saltos de línea con un marcador temporal
    feedback_final = feedback.replace('\n\n', '\n')
    return feedback_final

def convert_to_gift(questions):
    gift_format = ""
    wrong_answers = ""
    for question in questions:
        question_text = question.split("\n")[0].strip()
        question_text = re.sub(r"Question #\d+: ", "", question_text)
        
        answers = re.findall(r" - (A|B|C|D|E)\. (.*?)\n", question)
        correct_answer = re.search(r"Correct Answer: ([A-E]+)", question).group(1)
        
        gift_format += "::{}:: {} {{\n".format(question_text[:10] + "...", question_text)
        
        if len(correct_answer) == 1:
            # Single correct answer
            for answer in answers:
                if answer[0] == correct_answer:
                    gift_format += "=%s. %s\n" % (answer[0], answer[1])
                    correct_answer_full = "%s. %s\n" % (answer[0], answer[1])
                else:
                    gift_format += "~%s. %s\n" % (answer[0], answer[1])
                    wrong_answers += "%s. %s\n" % (answer[0], answer[1])
        else:
            # Multiple correct answers
            correct_answers = list(correct_answer)
            num_correct = len(correct_answers)
            for answer in answers:
                if answer[0] in correct_answers:
                    gift_format += "~%{}% {}. {}\n".format(100 / num_correct, answer[0], answer[1])
                    correct_answer_full += "{} {}. {}\n".format(100 / num_correct, answer[0], answer[1])
                    correct_answer_full += " and "
                else:
                    gift_format += "~%-100% {}. {}\n".format(answer[0], answer[1])
                    wrong_answers += " {}. {}\n".format(answer[0], answer[1])
        feedback = get_feedback(question_text, correct_answer_full, wrong_answers)
        gift_format += f"#### {feedback}\n}}\n\n" 

    return gift_format

def read_questions_from_file(input_file):
    with open(input_file, 'r') as file:
        content = file.read()
    
    questions = content.split("========================================")
    questions = [q.strip() for q in questions if q.strip()]
    
    return questions

def main(input_file, output_file):
    questions = read_questions_from_file(input_file)
    gift_text = convert_to_gift(questions)
    
    with open(output_file, 'w') as file:
        file.write(gift_text)

    print(f"Conversion completed. Check the {output_file} file.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert questions to GIFT format.")
    parser.add_argument("input_file", help="The input file containing the questions.")
    parser.add_argument("output_file", help="The output file to save the GIFT formatted questions.")
    
    args = parser.parse_args()
    
    main(args.input_file, args.output_file)

