# Created by Nikolay Pakhomov 30.07.2024
import aspose.pdf as ap
import random
import sys
import os


def create_total_report(report_path, after, before):
    file_name = "report" + str(random.randint(0, sys.maxsize)) + ".pdf"
    path_to_report = os.path.join(report_path, file_name)
    document = ap.Document()
    # Add page
    page = document.pages.add()
    # Initialize text_fragment object
    text_fragment = ap.text.TextFragment("Hello,world!")
    # Add text fragment to new page
    page.paragraphs.add(text_fragment)
    # Save updated PDF
    document.save(path_to_report)
    return path_to_report, file_name


def create_trainer_report(report_path, trainer_id, after, before):
    file_name = "report" + str(random.randint(0, sys.maxsize)) + ".pdf"
    path_to_report = os.path.join(report_path, file_name)
    document = ap.Document()
    # Add page
    page = document.pages.add()
    # Initialize text_fragment object
    text_fragment = ap.text.TextFragment("Hello,world!")
    # Add text fragment to new page
    page.paragraphs.add(text_fragment)
    # Save updated PDF
    document.save(path_to_report)
    return path_to_report, file_name


def create_client_report(report_path, client_id, after, before):
    file_name = "report" + str(random.randint(0, sys.maxsize)) + ".pdf"
    path_to_report = os.path.join(report_path, file_name)
    document = ap.Document()
    # Add page
    page = document.pages.add()
    # Initialize text_fragment object
    text_fragment = ap.text.TextFragment("Hello,world!")
    # Add text fragment to new page
    page.paragraphs.add(text_fragment)
    # Save updated PDF
    document.save(path_to_report)
    return path_to_report, file_name
