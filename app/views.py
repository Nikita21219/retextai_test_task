from flask import render_template, request, send_from_directory, jsonify, url_for
from tasks import *
from celery.result import AsyncResult


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('post reauest')
        f = request.files['file']
        try:
            docx_files.save(f)
            task = translate.delay(f.filename)
            return render_template("index.html", task_id=task.id)
            # return jsonify(task_id=task.id)
        except:
            return render_template('index.html', error="Произошла ошибка при загрузке файла")
    return render_template('index.html')


@app.route('/status/<task_id>')
def task_status(task_id):
    # проверяем статус задачи с указанным ID
    status = AsyncResult(task_id, app=celery).status
    print(f"\nCheck status: {status} task_id: {task_id}\n")

    if status == 'SUCCESS':
        return render_template('index.html', filename="en_retext_ai.docx")
        # return render_template('success.html', file_url=url_for('download_file', filename='processed_file.csv'))

    # если задача еще не выполнена, отображаем сообщение ожидания
    print("\nзадача еще не выполнена\n")
    return render_template('index.html', task_id=task_id, error="Waiting...")


@app.route(f'/{DOC_OUT_DIR}/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=DOC_OUT_DIR, path=filename)
