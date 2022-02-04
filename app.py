from flask import Flask,flash,session, request,redirect,url_for,render_template
from werkzeug.utils import secure_filename
from flask_session import Session
import os
import wave
import single_file_inference as inf
import random

from single_file_inference import Wav2VecCtc

UPLOAD_FOLDER = 'uploads/audios/'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict(file):
    transcript = ''

    if file:
        file_name = str(random.randint(0,10000))
        file.save(file_name)
        model_path = 'final_model.pt'
        dict_path = 'dict.ltr.txt'
        wav_path = file_name
        cuda = False
        decoder = 'kenlm'
        half = False
        lexicon_path = 'lexicon.lst'
        lm_path = 'lm.binary'
        transcript = inf.parse_transcription(model_path, dict_path, wav_path, cuda, decoder, lexicon_path, lm_path, half)
        os.remove(file_name)
    
    return transcript

@app.route('/',methods=["GET","POST"])
def home():
    output = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = file.filename
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output=predict(file)
    return render_template('index.html',output=output)

if __name__ == "__main__":
    sess = Session()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run(host ='0.0.0.0', debug=True,port=8888)
