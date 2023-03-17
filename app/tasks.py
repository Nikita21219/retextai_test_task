from app import *
from file_translator import FileTranslator
from flask import render_template


@celery.task
def translate(filename):
    src = f"{DOC_IN_DIR}/{filename}"
    dest = f"{DOC_OUT_DIR}/{PREFIX}_{filename}"
    ft = FileTranslator()
    ft.translate(src, dest)
