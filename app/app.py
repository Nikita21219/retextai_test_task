from flask import Flask
from flask_uploads import UploadSet, DOCUMENTS, configure_uploads
import os

DOC_IN_DIR = 'docs/in'
DOC_OUT_DIR = 'docs/out'
PREFIX = 'en'

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 15000000
app.config['UPLOADED_DOCUMENTS_DEST'] = os.path.join(basedir, DOC_IN_DIR)
app.config['UPLOADED_DOCUMENTS_ALLOW'] = set(['docx'])
docx_files = UploadSet('documents', DOCUMENTS)
configure_uploads(app, docx_files)


if __name__ == "__main__":
    app.run()
