import os, secrets, librosa, youtube_dl
import soundfile as sf

def yt_source_split(url, filename='music', key = ''):
    if key == '':
        key = secrets.token_urlsafe(8)
    filename = filename + '-' + key
    os.system("youtube-dl -o \'" + filename + ".%(ext)s\' -x --audio-format \'wav\' \'" + url + "\' ; youtube-dl -e \'" + url + "\' > \'title.txt\'")

    f = open("title.txt", "r")
    title = f.read()
    f.close()
    os.system("rm title.txt")
    
    if os.path.exists(filename + '.wav'):
        os.system("spleeter separate -i " + filename + ".wav -o static/ext/ -p spleeter:4stems ; mv " + filename + ".wav static/ext/" + filename + "/" + filename + ".wav")
        return key, title
    return [-1]*2

def yt_sample_split(url_1, url_2):

    key_, title_1 = yt_source_split(url_1, 'music1')
    if key_ == -1:
        return [-1]*3
    key, title_2 = yt_source_split(url_2, 'music2', key_)
    if key == -1:
        os.system("rm -r static/ext/music1-" + key_)
        return [-1]*3
    return key, title_1, title_2

def wav_source_split(filename, key = ''):
    if key == '':
        key = secrets.token_urlsafe(8)
    filename = filename + '-' + key
    os.system("spleeter separate -i static/ext/" + filename + ".wav -o static/ext/ -p spleeter:4stems")
    os.system("mv static/ext/" + filename + ".wav static/ext/" + filename + "/" + filename + ".wav")


def combinate_stems(key):
    vocals, sr = librosa.load("static/ext/music-" + key + "/vocals.wav")
    drums, _   = librosa.load("static/ext/music-" + key + "/drums.wav")
    bass, _    = librosa.load("static/ext/music-" + key + "/bass.wav")
    others, _  = librosa.load("static/ext/music-" + key + "/other.wav")

    for v in range(2):
        for d in range(2):
            for b in range(2):
                for o in range(2):
                    if v == d == b == o == 0:
                        continue
                    else:
                        audio = 0
                        if v == 1:
                            audio += vocals
                        if d == 1:
                            audio += drums
                        if b == 1:
                            audio += bass
                        if o == 1:
                            audio += others
                        sf.write("static/ext/music-" + key + "/" + str(v)+str(d)+str(b)+str(o) + '.wav', audio, sr)
    
    os.system("rm static/ext/music-" + key + "/vocals.wav")
    os.system("rm static/ext/music-" + key + "/drums.wav")
    os.system("rm static/ext/music-" + key + "/bass.wav")
    os.system("rm static/ext/music-" + key + "/other.wav")