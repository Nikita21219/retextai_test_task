from flask import render_template, request, send_from_directory
from app import *
from file_translator import FileTranslator
import flask_uploads


def translate(filename):
    src = f"{DOC_IN_DIR}/{filename}"
    dest = f"{DOC_OUT_DIR}/{PREFIX}_{filename}"
    ft = FileTranslator()
    ft.translate(src, dest)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        try:
            docx_files.save(request.files['file'])
            translate(f.filename)
        except:
            print("ERROR to upload") # TODO fix error
        return render_template('index.html', filename=f"{PREFIX}_{f.filename}")
    return render_template('index.html')


@app.route(f'/{DOC_OUT_DIR}/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=DOC_OUT_DIR, path=filename)
