from app import *
from file_translator import FileTranslator
from flask import render_template
import os


@celery.task
def translate(filename):
    src = f"{DOC_IN_DIR}{filename}"
    dest = f"{DOC_OUT_DIR}{PREFIX}_{filename}"
    ft = FileTranslator()
    ft.translate(src, dest)
    os.remove(os.path.join(basedir, src))


@celery.task
def delete_file(filename):
    try:
        os.remove(f"{os.path.join(basedir, DOC_OUT_DIR)}{filename}")
    except FileNotFoundError:
        return
