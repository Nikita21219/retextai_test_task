import magic
import io
from flask_uploads import UploadSet, DOCUMENTS


docx_files = UploadSet('documents', DOCUMENTS)


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
