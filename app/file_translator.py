from docx import Document
from googletrans import Translator


class FileTranslator:
    def __init__(self):
        self.translator = Translator()
        self.dest = 'en'

    def translate_text(self, text):
        return self.translator.translate(text, dest=self.dest).text

    def translate_table(self, table):
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.text = self.translate_text(paragraph.text)

    def translate(self, input_path, output_path):
        doc = Document(input_path)
        for paragraph in doc.paragraphs:
            paragraph.text = self.translate_text(paragraph.text)

        for table in doc.tables:
            self.translate_table(table)

        doc.save(output_path)
