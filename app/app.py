from flask import Flask
from flask_uploads import UploadSet, DOCUMENTS, configure_uploads
import os
from celery import Celery
from flask import render_template, request, send_from_directory, jsonify, url_for, session
from tasks import *
from celery.result import AsyncResult
# from utils import allowed_file
import magic
import io


def allowed_file(file):
    if not docx_files.file_allowed(file, file.filename):
        return False
    buffer = io.BytesIO()
    file.save(buffer)
    mime = magic.from_buffer(buffer.getvalue(), mime=True)
    file.stream.seek(0)
    allowed_mimes = [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword'
    ]
    return mime in allowed_mimes


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

docx_files = UploadSet('documents', DOCUMENTS)
configure_uploads(app, docx_files)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


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


@app.route(f'/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    delete_file.apply_async(args=[filename, ], countdown=600)
    return send_from_directory(directory=DOC_OUT_DIR, path=filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
