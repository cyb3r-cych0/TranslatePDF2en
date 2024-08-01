from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from googletrans import Translator
import time
from fpdf import FPDF


def show_spinner():
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧"]
    for _ in range(10):
        for char in spinner:
            print(f"\rRunning... {char}", end="")
            time.sleep(0.1)
    print("\rJob Complete! \n")
    # time.sleep(0.5)


""" Extract Text From PDF """


def convert_pdf_to_txt(path):
    try:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        # codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""  # If the PDF is password-protected
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)
            text = retstr.getvalue()
            show_spinner()

        fp.close()
        device.close()
        retstr.close()
        return text

    except FileNotFoundError:
        print("Error: The specified PDF file was not found.")
        return None
    except Exception as e:
        print(f"Error during PDF extraction: {e}")
        return None


print('------' * 10)
print('\t\t Starting Extraction...')
print('------' * 10)

pdf_text = convert_pdf_to_txt('lorem-ipsum.pdf')
# print(f'\n\n\n{pdf_text}\n\n\n')

print('------' * 10)
print('\t\t Extraction Completed...')
print('------' * 10)

""" Translate Extracted Text To English Using GoogleTranslateAPI"""


def translate_non_english_to_english(text):
    try:
        translator = Translator()

        # Split the text into sentences (you may need to adjust this based on your PDF structure)
        sentences = text.split('. ')  # Split by period and space

        translated_text = []
        for sentence in sentences:
            detected_lang = translator.detect(sentence).lang
            if detected_lang != 'en':
                translated_sentence = translator.translate(sentence, dest='en').text
                translated_text.append(translated_sentence)
            else:
                translated_text.append(sentence)
            show_spinner()
        return '. '.join(translated_text)
    except Exception as e:
        print(f"Error during translation: {e}")
        return None


print('------' * 10)
print('\t\t Starting Translation...')
print('------' * 10)

translated_pdf_text = translate_non_english_to_english(pdf_text)
# print(f'\n\n\n{translated_pdf_text}\n\n\n')

print('------' * 10)
print(f'\t\t Translation Completed...')
print('------' * 10)

""" Create PDF File With Translated Text """


def create_pdf_with_text(text, output_filename):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        # Split the translated text into lines (you may need to adjust this based on your content)
        lines = text.split("\n")

        for line in lines:
            # pdf.cell(200, 10, txt=line, ln=1, align="C")
            pdf.multi_cell(0, 8, txt=line, align="L")
            show_spinner()

        # Save the PDF with the specified filename
        pdf.output(output_filename)
    except Exception as e:
        print(f"Error during PDF creation: {e}")


print('------' * 10)
print('\t\t Creating Translated PDF...')
print('------' * 10)

translated_text_data = translated_pdf_text
create_pdf_with_text(translated_text_data, "translated_output.pdf")

print('------' * 10)
print(f'\t\t PDF Creation Completed...')
print('------' * 10)
