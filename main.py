import os
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
import string
import random



#UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "upload")
UPLOAD_FOLDER = "/var/www/html/tlog/tlog/uploaded"
ALLOWED_EXTENSIONS = {'bin', 'log', 'tlog'}



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print("files:", request.files)
        _id = id_generator()
        filename = None
        try:
            path = UPLOAD_FOLDER
            if not os.path.exists(path):
                os.makedirs(path)
            for key, item in request.files.items():
                extension = item.filename.split(".")[-1]
                filename = _id + '.' + extension
                item.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as e:
            return "error " + str(e)
        return filename
    return "bad request"

@app.route('/uploaded/<filename>')
def servefile(filename):
    print(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)

app.run(host="localhost", port=8001)

