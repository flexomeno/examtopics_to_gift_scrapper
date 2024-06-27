from _classes import CardList
import os
import subprocess

RES_DIR = "./res"  # directorio de recursos
OUTPUT_FILE = "extracted_questions_and_answers.txt"  # nombre del archivo de salida
OTHER_SCRIPT = "convert.py"  # nombre del otro script de Python
GIFT_OUTPUT_FILE = "questions_in_gift_format.txt"  # archivo de salida para el formato GIFT

def extract_qa_to_file():
    card_list = CardList(RES_DIR)
    qa_list = card_list.extract_questions_and_answers()

    with open(OUTPUT_FILE, "w", encoding="utf8") as file:
        for qa in qa_list:
            file.write(f"Question {qa['question_number']}: {qa['question']}\n")
            file.write("Answers:\n")
            for answer in qa['answers']:
                file.write(f" - {answer}\n")
            file.write(f"Correct Answer: {qa['correct_answer']}\n")
            file.write("=" * 40 + "\n\n")

    print(f"Questions and answers have been written to {OUTPUT_FILE}")

    # Ejecutar otro script de Python
    result = subprocess.run(
        ["python3", OTHER_SCRIPT, OUTPUT_FILE, GIFT_OUTPUT_FILE], 
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == "__main__":
    extract_qa_to_file()
