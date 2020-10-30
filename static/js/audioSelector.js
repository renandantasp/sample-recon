var source_s = document.querySelector('#_0000');
const vocal_box = document.querySelector('#vocalC');
const drums_box = document.querySelector('#drumsC');
const bass_box = document.querySelector('#bassC');
const other_box = document.querySelector('#otherC');
var str = '#';
var v = 0;
var d = 0;
var b = 0;
var o = 0;


function update_audio(){
        source_s.style.display = "none";
        str = '#_' + v.toString() + d.toString() + b.toString() + o.toString();
        source_s = document.querySelector(str);
        source_s.style.display = "inline";
}

if(vocal_box){
    vocal_box.addEventListener('change',function(e){
        if(vocal_box.checked){
            v = 1;
            update_audio();
        }
        else{
            v = 0;
            update_audio();
        }
    });
}

if(drums_box){
    drums_box.addEventListener('change',function(e){
        if(drums_box.checked){
            d = 1;
            update_audio();
        }
        else{
            d = 0;
            update_audio();
        }
    });
}

if(bass_box){
    bass_box.addEventListener('change',function(e){
        if(bass_box.checked){
            b = 1;
            update_audio();
        }
        else{
            b = 0;
            update_audio();
        }
    });
}    
if(other_box){
    other_box.addEventListener('change',function(e){
        if(other_box.checked){
            o = 1;
            update_audio();
        }
        else{
            o = 0;
            update_audio();
        }
    });
}