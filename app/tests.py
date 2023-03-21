import os
import unittest
from file_translator import FileTranslator
import requests


def remove_files(folder):
    files_in = os.listdir(folder)
    for file in files_in:
        os.remove(folder + file)


class TestFileTranslator(unittest.TestCase):
    def setUp(self):
        self.ft = FileTranslator()
        self.doc_out_dir = 'docs/out/'

    def test_translate(self):
        self.assertFalse(self.ft.translate('', ''))
        self.assertFalse(self.ft.translate('not exists file', ''))
        self.assertFalse(self.ft.translate('', 'not exists file'))
        self.assertFalse(self.ft.translate('not exists file', 'not exists file'))
        self.assertFalse(self.ft.translate('/Users/a1/Downloads/001.mp4', 'out.docx'))
        self.assertTrue(self.ft.translate('docs/example/retext_ai.docx', self.doc_out_dir + 'out.docx'))

    def tearDown(self):
        remove_files(self.doc_out_dir)


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.host = 'http://localhost/'
        self.doc_in_dir = 'docs/in/'
        self.doc_out_dir = 'docs/out/'

    def test_index(self):
        # Get requests
        self.assertEqual(requests.get(self.host).status_code, 200)
        self.assertEqual(requests.get(self.host + "notfound").status_code, 404)
        # Post requests
        self.assertEqual(requests.post(self.host).status_code, 400)
        with open('docs/example/retext_ai.docx', 'rb') as f:
            self.assertEqual(requests.post(self.host, files={'file': f}).status_code, 200)

    def test_status(self):
        url = self.host + "status"
        self.assertEqual(requests.get(url).status_code, 500)

    def tearDown(self):
        remove_files(self.doc_in_dir)
        remove_files(self.doc_out_dir)


if __name__ == "__main__":
    unittest.main()
