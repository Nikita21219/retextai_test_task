from flask import render_template, request, send_from_directory, jsonify, url_for, session
from tasks import *
from celery.result import AsyncResult
from utils import allowed_file


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
