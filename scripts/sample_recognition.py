import librosa, librosa.feature
import numpy as np
import soundfile as sf
from scripts.simpleab import simpleab

def find_coords(mp):
    num_rows, num_cols = np.shape(mp)
    sim_coords = list()
    row, col = [num_rows-1, num_cols-1]
    while(row>0 or col>0):
        on_diag = False
        prox_jump = 8
        if row>0:
            i,j = [row, 0]
        else:
            i,j = [0, col]
        while(i < num_rows and j < num_cols):
            if on_diag == False:
                if(mp[i][j] <= 120):
                    on_diag = True
                    start = [i,j]
                    size = 1
                    intensity = mp[i][j]
            else:
                if(mp[i][j] <= 120):
                    size += 1
                    intensity += mp[i][j]
                else:
                    if size > 80:
                        med = intensity/size
                        sim_coords.append([size, med, [start, [i,j]]])
                        prox_jump = 8
                    on_diag = False
            i += 1
            j += 1
        if row>0:
            row = row-prox_jump if row-prox_jump>0 else 0
        else:
            col = col-prox_jump if col-prox_jump>0 else 0
    
    if sim_coords == []:
        return -1
    sim_coords = np.sort(sim_coords, axis=0)[::-1]
    sim_coords = sim_coords[:,1:][::]
    sim_coords = np.sort(sim_coords, axis=0, kind='mergesort')
    sim_coords = sim_coords[:,1][::]
    
    return sim_coords   

def check_sim(key, vocal, bass, other):
    music_1, sr = librosa.load("static/ext/music1-" + key + "/music1-" + key + ".wav")
    music_2, sr = librosa.load("static/ext/music2-" + key + "/music2-" + key + ".wav")
    msg = np.zeros(3, int)
    if vocal == 'true': msg[0] = make_sim(key, "vocals", music_1, music_2, sr)
    if bass  == 'true': msg[1] = make_sim(key, "bass",   music_1, music_2, sr)
    if other == 'true': msg[2] = make_sim(key, "other",  music_1, music_2, sr)
    if msg.any() == 1:
        return ''
    if msg.any() == -1:
        return 'Não foi encontrado nenhum caso de sampling.'
    return 'Nenhuma faixa foi selecionada.'

def make_sim(key, stem, music_1, music_2, sr):

    stem_1, _ = librosa.load("static/ext/music1-" + key + "/" + stem + ".wav")
    stem_2, _ = librosa.load("static/ext/music2-" + key + "/" + stem + ".wav")

    chroma_1 = librosa.feature.chroma_cens(y=stem_1, sr=sr)
    chroma_2 = librosa.feature.chroma_cens(y=stem_2, sr=sr)

    mp, mpindex = simpleab(chroma_1, chroma_2, 215)
    
    coords = find_coords(mp)
    if np.size(coords) == 1:
        return -1
    
    rows, cols = np.shape(mp)
    for i in range(np.size(coords)):
        st_1 = coords[i][0][0]
        en_1 = coords[i][1][0]

        st_2 = coords[i][0][1]
        en_2 = coords[i][1][1]

        time_1 = np.size(music_1) / sr
        time_2 = np.size(music_2) / sr

        second_1 = rows / time_1
        second_2 = cols / time_2

        stamp_1 = [int((st_1 / second_1)*sr), int((en_1 / second_1)*sr)]
        stamp_2 = [int((st_2 / second_2)*sr), int((en_2 / second_2)*sr)]
        
        crop_m1 = music_1[stamp_1[0]:stamp_1[1]]
        crop_s1 = stem_1[stamp_1[0]:stamp_1[1]]
        
        crop_m2 = music_2[stamp_2[0]:stamp_2[1]]
        crop_s2 = stem_2[stamp_2[0]:stamp_2[1]]

        if crop_s1.max() < 0.25 or crop_s2.max() < 0.25:
            continue
        else:
            sf.write("static/ext/music1-" + key + "/" + stem + "_full_crop.wav", crop_m1, sr)
            sf.write("static/ext/music1-" + key + "/" + stem + "_ext_crop.wav",  crop_s1, sr)
            sf.write("static/ext/music2-" + key + "/" + stem + "_full_crop.wav", crop_m2, sr)
            sf.write("static/ext/music2-" + key + "/" + stem + "_ext_crop.wav",  crop_s2, sr)
            return 1
    return -1
        
