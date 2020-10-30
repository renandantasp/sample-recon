import os, secrets
from flask import Flask, render_template, url_for, flash, redirect, Response,request
from flask_assets import Bundle, Environment
from werkzeug.utils import secure_filename

from scripts.splitter import yt_source_split, wav_source_split, yt_sample_split, combinate_stems
from scripts.utility import is_supported
from scripts.sample_recognition import check_sim

UPLOAD_FOLDER  = 'static/ext/'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER']  = UPLOAD_FOLDER

js = Bundle('js/reminder.js', 'js/wavHandler.js', 'js/audioSelector.js', 'js/sample_audio_selector.js', output = 'gen/main.js')
assets = Environment(app)
assets.register('main_js',js)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def _home():
    return redirect(url_for("home"))

@app.route("/home", methods=['POST','GET'])
def home():
    return render_template('home.html',title='Página Inicial',flag=1)

@app.route("/about")
def about():
    return render_template('about.html', title='Sobre')


@app.route("/yt_split",  methods=['POST','GET'])
def yt_split():
    if request.method == "POST":
        if is_supported(request.form["ytLink"]):
            #clean_folder()
            ytLink = request.form["ytLink"]
            key, video_title = yt_source_split(ytLink)
            if key == -1:
                return render_template('error.html', title='Erro')
            combinate_stems(key)
            _, url = ytLink.split("watch?v=",1)
            url = "https://www.youtube.com/embed/" + url[0:11]
            os.system("(sleep 100 ; rm -r static/ext/music-" + key + ") &")
            return render_template('yt_split.html', title= 'Separação de áudio', url=url, video_title=video_title, key=key)
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/wav_split",  methods=['POST','GET'])
def wav_split():
    if request.method == "POST":
        #clean_folder()
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for("home"))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for("home"))
        if file and allowed_file(file.filename):
            key = secrets.token_urlsafe(8)
            filename = 'music-' + key + '.wav'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        wav_source_split('music', key)
        combinate_stems(key)
        os.system("(sleep 100 ; rm -r static/ext/music1-" + key + ") &")
        return render_template('wav_split.html', title='Separação de áudio', key=key)
    else:
        return redirect(url_for("home"))

@app.route("/yt_sampling", methods=['POST', 'GET'])
def yt_sampling():
    if request.method == "POST":
        if is_supported(request.form["url_1"]) and is_supported(request.form["url_2"]):
            #clean_folder()
            yt_url_1 = request.form["url_1"]
            yt_url_2 = request.form["url_2"]
               
            key, video_title_1, video_title_2 = yt_sample_split(yt_url_1, yt_url_2)
            if key == -1:
                return render_template('error.html', title='Erro')
            is_sampled = check_sim(key, request.form.get('vocal_box'), request.form.get('bass_box'), request.form.get('other_box'))
            
            _, url_1 = yt_url_1.split("watch?v=",1)
            _, url_2 = yt_url_2.split("watch?v=",1)
            
            url_1 = "https://www.youtube.com/embed/" + url_1[0:11]
            url_2 = "https://www.youtube.com/embed/" + url_2[0:11]
            os.system("(sleep 100 ; rm -r static/ext/music1-" + key + ") &")
            os.system("(sleep 100 ; rm -r static/ext/music2-" + key + ") &")
            return render_template('yt_sample.html', title='Reconhecimento de sample', url_1 = url_1, url_2 = url_2, video_title_1 = video_title_1, video_title_2 = video_title_2, is_sampled = is_sampled)
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/wav_sampling", methods=['POST', 'GET'])
def wav_sampling():
    if request.method == "POST":
        #clean_folder()
        if 'file1' not in request.files or 'file2' not in request.files:
            flash('No file part')
            return redirect(url_for("home"))
        file1 = request.files['file1']
        file2 = request.files['file2']
        if file1.filename == '' or file2.filename == '':
            flash('No selected file')
            return redirect(url_for("home"))
        if file1 and allowed_file(file1.filename):
            key = secrets.token_urlsafe(8)
            filename = 'music1-' + key + '.wav'
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if file2 and allowed_file(file2.filename):
            filename = 'music2-' + key + '.wav'
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        wav_source_split('music1', key)
        wav_source_split('music2', key)
        is_sampled = check_sim(key, request.form.get('vocal_box'), request.form.get('bass_box'), request.form.get('other_box'))
        os.system("(sleep 100 ; rm -r static/ext/music1-" + key + ") &")
        os.system("(sleep 100 ; rm -r static/ext/music2-" + key + ") &")
        return render_template('wav_sample.html', title='Reconhecimento de sample', is_sampled = is_sampled, key=key)
    else:
        return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)