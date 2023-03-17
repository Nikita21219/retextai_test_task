from flask import render_template, request, send_from_directory, jsonify, url_for, session
from tasks import *
from celery.result import AsyncResult


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('post request')
        f = request.files['file']
        try:
            docx_files.save(f)
            task = translate.delay(f.filename)
            session['task_id'] = task.id
            return render_template("index.html")
            # return jsonify(task_id=task.id)
        except:
            return render_template('index.html', error="Произошла ошибка при загрузке файла")
    return render_template('index.html')


@app.route('/status')
def task_status():
    # проверяем статус задачи с указанным ID
    status = AsyncResult(session['task_id'], app=celery).status
    print(f"\nCheck status: {status} task_id: {session['task_id']}\n")

    if status == 'SUCCESS':
        link = "/" + DOC_OUT_DIR + "/" + "en_retext_ai.docx"
        return jsonify(status=status, link=link)

    return jsonify(status=status)


@app.route(f'/{DOC_OUT_DIR}/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    print("TEST!")
    return send_from_directory(directory=DOC_OUT_DIR, path=filename)
