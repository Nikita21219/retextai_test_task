from flask import Flask
import os
from celery import Celery
from flask import render_template, request, send_from_directory, jsonify, session
from flask_uploads import configure_uploads
from celery.result import AsyncResult
from file_translator import FileTranslator
from utils import *


# configs
DOC_IN_DIR = f'docs{os.sep}in{os.sep}'
DOC_OUT_DIR = f'docs{os.sep}out{os.sep}'
PREFIX = 'en'

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 15000000
app.config['UPLOADED_DOCUMENTS_DEST'] = os.path.join(basedir, DOC_IN_DIR)
app.config['CELERY_BROKER_URL'] = f'redis://{os.getenv("REDIS_HOST")}:6379/0'
app.config['CELERY_RESULT_BACKEND'] = f'redis://{os.getenv("REDIS_HOST")}:6379/0'

configure_uploads(app, docx_files)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# celery tasks
@celery.task
def translate(filename):
    src = f"{DOC_IN_DIR}{filename}"
    dest = f"{DOC_OUT_DIR}{PREFIX}_{filename}"
    ft = FileTranslator()
    ft.translate(src, dest)
    delete_file.apply_async(args=[os.path.join(basedir, src), ], countdown=20)


@celery.task
def delete_file(filename):
    try:
        os.remove(f"{os.path.join(basedir, DOC_OUT_DIR)}{filename}")
    except FileNotFoundError:
        return


# routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file):
            filename = docx_files.save(file)
            task = translate.delay(filename)
            session['task_id'] = task.id
            session['filename'] = filename
            return render_template("index.html")
        else:
            return jsonify("Произошла ошибка при загрузке файла"), 403
    return render_template('index.html')


@app.route('/status')
def task_status():
    status = AsyncResult(session['task_id'], app=celery).status
    if status == 'SUCCESS':
        link = f"{PREFIX}_{session['filename']}"
        return jsonify(status=status, link=link)
    return jsonify(status=status)


@app.route(f'/<path:filename>', methods=['GET'])
def download(filename):
    delete_file.apply_async(args=[filename, ], countdown=20)
    return send_from_directory(directory=DOC_OUT_DIR, path=filename)


if __name__ == "__main__":
    app.run()
