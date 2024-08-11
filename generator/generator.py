import json
import os
import random
import string
from collections import deque
from dotenv import load_dotenv
from docx import Document
from fpdf import FPDF
import pandas as pd
import csv
import zipfile
from PIL import Image
import numpy as np
import cv2
import xml.etree.ElementTree as ET

# Load configuration from .env file
load_dotenv()

BASE_PATH = os.getenv("BASE_PATH")
MAX_DEPTH = int(os.getenv("MAX_DEPTH"))
MAX_FILES = int(os.getenv("MAX_FILES"))
CREATION_PROBABILITY = float(os.getenv("CREATION_PROBABILITY"))
MIN_TEXT_LENGTH = int(os.getenv("MIN_TEXT_LENGTH"))
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH"))
MAX_FILES_PER_FOLDER = int(os.getenv("MAX_FILES_PER_FOLDER"))
MIN_FILES_PER_FOLDER = int(os.getenv("MIN_FILES_PER_FOLDER"))
LARGE_FILE_PROBABILITY = float(os.getenv("LARGE_FILE_PROBABILITY"))
LARGE_FILE_SIZE = int(os.getenv("LARGE_FILE_SIZE"))
SHOULD_CREATE_LARGE_FILES = os.getenv("SHOULD_CREATE_LARGE_FILES") == "true"
SHOULD_CREATE_WORD_FILES = os.getenv("SHOULD_CREATE_WORD_FILES") == "true"
PARSED_EXTENSIONS_PROBABILITIES = {
    "txt": 0.1,
    "docx": 0.1,
    "xlsx": 0.1,
    "pdf": 0.1,
    "csv": 0.1,
    "png": 0.1,
    "zip": 0.1,
    "avi": 0.1,
    "xml": 0.1,
    "json": 0.1,
}

print(f"BASE_PATH: {BASE_PATH}")
print(f"MAX_DEPTH: {MAX_DEPTH}")
print(f"MAX_FOLDERS: {MAX_FILES}")
print(f"CREATION_PROBABILITY: {CREATION_PROBABILITY}")
print(f"MIN_TEXT_LENGTH: {MIN_TEXT_LENGTH}")
print(f"MAX_TEXT_LENGTH: {MAX_TEXT_LENGTH}")
print(f"MAX_FILES_PER_FOLDER: {MAX_FILES_PER_FOLDER}")
print(f"MIN_FILES_PER_FOLDER: {MIN_FILES_PER_FOLDER}")
print(f"LARGE_FILE_PROBABILITY: {LARGE_FILE_PROBABILITY}")
print(f"LARGE_FILE_SIZE: {LARGE_FILE_SIZE}")
print(f"SHOULD_CREATE_LARGE_FILES: {SHOULD_CREATE_LARGE_FILES}")
print(f"SHOULD_CREATE_WORD_FILES: {SHOULD_CREATE_WORD_FILES}")
print(f"PARSED_EXTENSIONS_PROBABILITIES: {PARSED_EXTENSIONS_PROBABILITIES}")
input()


def generate_random_name(length=8):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_text(min_length=MIN_TEXT_LENGTH, max_length=MAX_TEXT_LENGTH):
    length = random.randint(min_length, max_length)
    return "".join(
        random.choices(
            string.ascii_letters + string.digits + string.punctuation + " ", k=length
        )
    )


def create_text_file(folder_path):
    text_file_name = generate_random_name(length=5) + ".txt"
    text_file_path = os.path.join(folder_path, text_file_name)
    with open(text_file_path, "w") as text_file:
        text_file.write(
            generate_large_text()
            if random.random() < LARGE_FILE_PROBABILITY and SHOULD_CREATE_LARGE_FILES
            else generate_random_text()
        )
    print(f"Created text file")


def create_word_document(folder_path):
    doc_file_name = generate_random_name(length=5) + ".docx"
    doc_file_path = os.path.join(folder_path, doc_file_name)

    if random.random() < LARGE_FILE_PROBABILITY:
        content = generate_large_text()
    else:
        content = generate_random_text()

    doc = Document()
    doc.add_paragraph(content)
    doc.save(doc_file_path)
    print(f"Created Word document")


def create_excel_file(folder_path):
    excel_file_name = generate_random_name(length=5) + ".xlsx"
    excel_file_path = os.path.join(folder_path, excel_file_name)

    if random.random() < LARGE_FILE_PROBABILITY and SHOULD_CREATE_LARGE_FILES:
        data = generate_large_dataframe()
    else:
        data = generate_random_dataframe()

    data.to_excel(excel_file_path, index=False)
    print(f"Created Excel file")


def generate_large_dataframe():
    # Generate a large DataFrame with random data
    return pd.DataFrame({
        'Column1': [generate_random_text() for _ in range(10000)],
        'Column2': [random.randint(1, 10000) for _ in range(10000)]
    })


def generate_random_dataframe():
    # Generate a smaller DataFrame with random data
    return pd.DataFrame({
        'Column1': [generate_random_text() for _ in range(40)],
        'Column2': [random.randint(1, 100) for _ in range(40)]
    })


def create_pdf_file(folder_path):
    pdf_file_name = generate_random_name(length=5) + ".pdf"
    pdf_file_path = os.path.join(folder_path, pdf_file_name)

    if random.random() < LARGE_FILE_PROBABILITY and SHOULD_CREATE_LARGE_FILES:
        content = generate_large_text()
    else:
        content = generate_random_text()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(pdf_file_path)
    print(f"Created PDF file")


def create_csv_file(folder_path):
    csv_file_name = generate_random_name(length=5) + ".csv"
    csv_file_path = os.path.join(folder_path, csv_file_name)

    if random.random() < LARGE_FILE_PROBABILITY and SHOULD_CREATE_LARGE_FILES:
        data = generate_large_csv_data()
    else:
        data = generate_random_csv_data()

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Column1", "Column2"])  # Header
        writer.writerows(data)

    print(f"Created CSV file")


def generate_large_csv_data():
    # Generate a large list of tuples with random data
    return [(generate_random_text(), random.randint(1, 10000)) for _ in range(10000)]


def generate_random_csv_data():
    # Generate a smaller list of tuples with random data
    return [(generate_random_text(), random.randint(1, 100)) for _ in range(1)]


def create_zip_file(folder_path):
    zip_file_name = generate_random_name(length=5) + ".zip"
    zip_file_path = os.path.join(folder_path, zip_file_name)

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        # Add a random text file
        text_file_name = generate_random_name(length=5) + ".txt"
        text_file_path = os.path.join(folder_path, text_file_name)
        with open(text_file_path, "w") as text_file:
            text_file.write(generate_random_text())
        zipf.write(text_file_path, arcname=text_file_name)

    print(f"Created zip file")


def create_image_file(folder_path):
    image_file_name = generate_random_name(length=5) + ".png"
    image_file_path = os.path.join(folder_path, image_file_name)

    # Create a random image using NumPy and Pillow
    width, height = 600, 600
    array = np.random.rand(height, width, 3) * 255
    image = Image.fromarray(array.astype('uint8')).convert('RGB')
    image.save(image_file_path)
    print(f"Created image file")


def create_video_file(folder_path):
    video_file_name = generate_random_name(length=5) + ".avi"
    video_file_path = os.path.join(folder_path, video_file_name)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_file_path, fourcc, 20.0, (640, 480))

    for _ in range(4):
        frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)  # Random frame
        out.write(frame)

    out.release()
    print(f"Created video file")


def create_xml_file(folder_path):
    xml_file_name = generate_random_name(length=5) + ".xml"
    xml_file_path = os.path.join(folder_path, xml_file_name)

    # Create the root element
    root = ET.Element("root")

    # Add some child elements with random data
    for i in range(1):  # Generate 5 random child elements
        child = ET.SubElement(root, "child")
        child.set("id", str(i))
        child.text = generate_random_text()

    # Convert the ElementTree to a string and write to a file
    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)

    print(f"Created XML file: {xml_file_name}")


def create_json_file(folder_path):
    json_file_name = generate_random_name(length=5) + ".json"
    json_file_path = os.path.join(folder_path, json_file_name)

    # Create a random dictionary
    data = {
        "id": generate_random_name(length=5),
        "description": generate_random_text(),
        "value": random.randint(1, 100),
    }

    # Write the dictionary to a JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Created JSON file: {json_file_name}")

def create_file(folder_path):
    extensions = list(PARSED_EXTENSIONS_PROBABILITIES.keys())
    weights = list(PARSED_EXTENSIONS_PROBABILITIES.values())

    extension = random.choices(extensions, weights=weights, k=1)[0]

    if extension == "txt":
        create_text_file(folder_path)
    elif extension == "docx":
        create_word_document(folder_path)
    elif extension == "xlsx":
        create_excel_file(folder_path)
    elif extension == "pdf":
        create_pdf_file(folder_path)
    elif extension == "csv":
        create_csv_file(folder_path)
    elif extension == "png":
        create_image_file(folder_path)
    elif extension == "zip":
        create_zip_file(folder_path)
    elif extension == "avi":
        create_video_file(folder_path)
    elif extension == "xml":
        create_xml_file(folder_path)
    elif extension == "json":
        create_json_file(folder_path)
    else:
        print(f"Unsupported extension: {extension}")


def generate_large_text(size=LARGE_FILE_SIZE):
    return "".join(
        random.choices(
            string.ascii_letters + string.digits + string.punctuation + " ", k=size
        )
    )


def create_nested_folders(
        base_path, max_depth, max_files, creation_probability=CREATION_PROBABILITY
):
    stack = deque([(base_path, 0)])
    total_folders_created = 0
    base = base_path, 0
    total_files_created = 0

    while total_files_created < max_files:
        current_path, current_depth = stack.pop() if stack else base

        if current_depth < max_depth:
            # Decide randomly whether to create a branch
            if random.random() < creation_probability:
                try:
                    folder_name = generate_random_name()
                    folder_path = os.path.join(current_path, folder_name)
                    os.makedirs(folder_path, exist_ok=False)
                    total_folders_created += 1
                    print(f"folders:{total_folders_created} files:{total_files_created}")

                    # Create multiple files for each folder
                    for i in range(
                            random.randint(MIN_FILES_PER_FOLDER, MAX_FILES_PER_FOLDER)
                    ):
                        # Create a text/docx file with random content inside the folder
                        create_file(folder_path)
                        total_files_created += 1
                    # Add new branch to stack
                    stack.append((folder_path, current_depth + 1))
                except FileExistsError:
                    print(f"Folder already exists: {folder_path}")

    print(f"Nested folder structure created under {base_path}")
    print(f"created {total_folders_created} folders and {total_files_created} files")


def main():
    base_path = BASE_PATH
    max_depth = MAX_DEPTH
    num_files = MAX_FILES

    create_nested_folders(base_path, max_depth, num_files)
    print(f"Nested folder structure created under {base_path}")


if __name__ == "__main__":
    main()
