""" Function File to Detect Languages in a File """

import os
import fitz  # PyMuPDF
from langdetect import detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from bs4 import BeautifulSoup
import docx

# Ensure the results are consistent
DetectorFactory.seed = 0


class LanguageDetector:
    """
    A class to detect the language of text content from various file types including PDF, HTML, TXT, and DOCX.

    Methods
    -------
    extract_text_from_pdf(file_path) : static method
        Extracts text from a PDF file.

    extract_text_from_html(file_path) : static method
        Extracts text from an HTML file.

    extract_text_from_txt(file_path) : static method
        Extracts text from a TXT file.

    extract_text_from_docx(file_path) : static method
        Extracts text from a DOCX file.

    detect_languages(text) : static method
        Detects the languages of a given text.

    detect_language_from_file(file_path) : class method
        Detects the language of a file based on its content.

    detect_primary_language_from_file(file_path) : class method
        Detects the primary language of a file based on its content.
    """

    supported_languages = [
        "af",
        "ar",
        "bg",
        "bn",
        "ca",
        "cs",
        "cy",
        "da",
        "de",
        "el",
        "en",
        "es",
        "et",
        "fa",
        "fi",
        "fr",
        "gu",
        "he",
        "hi",
        "hr",
        "hu",
        "id",
        "it",
        "ja",
        "kn",
        "ko",
        "lt",
        "lv",
        "mk",
        "ml",
        "mr",
        "ne",
        "nl",
        "no",
        "pa",
        "pl",
        "pt",
        "ro",
        "ru",
        "sk",
        "sl",
        "so",
        "sq",
        "sv",
        "sw",
        "ta",
        "te",
        "th",
        "tl",
        "tr",
        "uk",
        "ur",
        "vi",
        "zh-cn",
        "zh-tw",
    ]

    def __init__(self):
        pass

    @staticmethod
    def extract_text_from_pdf(file_path):
        """
        Extract text from a PDF file.

        Parameters
        ----------
        file_path : str
            The path to the PDF file.

        Returns
        -------
        str
            The extracted text from the PDF.
        """
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    @staticmethod
    def extract_text_from_html(file_path):
        """
        Extract text from an HTML file.

        Parameters
        ----------
        file_path : str
            The path to the HTML file.

        Returns
        -------
        str
            The extracted text from the HTML.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "lxml")
            text = soup.get_text()
        return text

    @staticmethod
    def extract_text_from_txt(file_path):
        """
        Extract text from a TXT file.

        Parameters
        ----------
        file_path : str
            The path to the TXT file.

        Returns
        -------
        str
            The extracted text from the TXT.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        return text

    @staticmethod
    def extract_text_from_docx(file_path):
        """
        Extract text from a DOCX file.

        Parameters
        ----------
        file_path : str
            The path to the DOCX file.

        Returns
        -------
        str
            The extracted text from the DOCX.
        """
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    @staticmethod
    def detect_languages(text):
        """
        Detect the languages of a given text.

        Parameters
        ----------
        text : str
            The text to detect the languages of.

        Returns
        -------
        list
            A list of LangDetectResult objects with 'lang' and 'prob' attributes.
        """
        try:
            languages = detect_langs(text)
            return languages
        except LangDetectException:
            return []

    @classmethod
    def detect_languages_from_file(cls, file_path):
        """
        Detect the language of a file.

        Parameters
        ----------
        file_path : str
            The path to the file.

        Returns
        -------
        list
            A list of LangDetectResult objects with 'lang' and 'prob' attributes.
        """
        _, ext = os.path.splitext(file_path)
        if ext.lower() == ".pdf":
            text = cls.extract_text_from_pdf(file_path)
        elif ext.lower() in [".html", ".htm"]:
            text = cls.extract_text_from_html(file_path)
        elif ext.lower() == ".txt":
            text = cls.extract_text_from_txt(file_path)
        elif ext.lower() == ".docx":
            text = cls.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        languages = cls.detect_languages(text)
        return languages

    @classmethod
    def detect_primary_language_from_file(cls, file_path):
        """
        Detect the primary language of a file.

        Parameters
        ----------
        file_path : str
            The path to the file.

        Returns
        -------
        str
            The language code of the primary language.
        """
        languages = cls.detect_languages_from_file(file_path)
        if languages:
            primary_language = max(languages, key=lambda x: x.prob)
            return primary_language.lang
        return None


def main(file_path):
    """
    Main function to detect the language of a file.

    Parameters
    ----------
    file_path : str
        The path to the file.

    Returns
    -------
    None
    """
    languages = LanguageDetector.detect_language_from_file(file_path)
    if languages:
        print("Detected Languages:")
        for language in languages:
            print(f" - Language: {language.lang}, Probability: {language.prob:.2f}")
    else:
        print("No language detected or the text is too ambiguous.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python language_detector.py <path_to_file>")
    else:
        file_path = sys.argv[1]
        main(file_path)
