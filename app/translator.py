import deepl
from conf import *


class Translator:
    def __init__(self):
        self.target_lang = "EN-US"
        self.translator = deepl.Translator(API_KEY)

    def translate(self, input_path: str, output_path: str):
        try:
            self.translator.translate_document_from_filepath(
                input_path,
                output_path,
                target_lang=self.target_lang,
            )

            with open(input_path, "rb") as in_file, open(output_path, "wb") as out_file:
                self.translator.translate_document(
                    in_file,
                    out_file,
                    target_lang=self.target_lang,
                )

        except deepl.DocumentTranslationException as error:
            doc_id = error.document_handle.id
            doc_key = error.document_handle.key
            print(f"Error after uploading ${error}, id: ${doc_id} key: ${doc_key}")

        except deepl.DeepLException as error:
            print(error)


if __name__ == "__main__":
    input_path = 'docs/1.docx'
    output_path = 'docs/out.docx'
    t = Translator()
    t.translate(input_path, output_path)
