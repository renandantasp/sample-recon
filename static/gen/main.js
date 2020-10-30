var trigger = document.querySelectorAll('.trigger');
var reminder = document.querySelectorAll('#reminder');

function reminder(){
    reminder[0].setAttribute("hidden", true);
    reminder[1].setAttribute("hidden", true);
}

if(trigger[0] || trigger[1]){
    trigger[0].addEventListener('click',function(e){
        reminder[0].removeAttribute("hidden");
    });
    trigger[1].addEventListener('click',function(e){
        reminder[0].removeAttribute("hidden");
    });
}
if(trigger[2] || trigger[3]){
    trigger[2].addEventListener('click',function(e){
        reminder[1].removeAttribute("hidden");
    });
    trigger[3].addEventListener('click',function(e){
        reminder[1].removeAttribute("hidden");
    });
}


var file_text = document.querySelectorAll('#fileText');
var file_button = document.querySelectorAll('#fileButton');


if (file_button[0]){
    file_button[0].addEventListener("change",function(e){
        console.log(file_button[0].value);
        if (file_button[0].value){
            file_text[0].innerText = file_button[0].value.substr(-(file_button[0].value.length-12)); 
        }
        else{
            file_text[0].innerText = "Insert a .wav file...";
        }
    });
}
if (file_button[1]){
    file_button[1].addEventListener("change",function(e){
        console.log(file_button[1].value);
        if (file_button[1].value){
            file_text[1].innerText = file_button[1].value.substr(-(file_button[1].value.length-12)); 
        }
        else{
            file_text[1].innerText = "Insert a .wav file...";
        }
    });
}
if (file_button[2]){    
    file_button[2].addEventListener("change",function(e){
        console.log(file_button[2].value);
        if (file_button[2].value){
            file_text[2].innerText = file_button[2].value.substr(-(file_button[2].value.length-12)); 
        }
        else{
            file_text[2].innerText = "Insert a .wav file...";
        }
    });

}

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
var old_sample_id = '#full_vocal'
const track = document.getElementsByName("track");
const stem = document.getElementsByName("stem");
var track_value = 'full_';
var stem_value = 'vocal';
var sample_id = "_";


function update_sample_audio(){
        var old_sample_arr = document.querySelectorAll(old_sample_id);
        for(var i = 0; i<old_sample_arr.length; i++){
            old_sample_arr[i].style.display = 'none';
        }
        //sample_s.style.display = "none";
        sample_id = '#' + track_value + stem_value;
        sample_id_arr = document.querySelectorAll(sample_id);
        console.log(old_sample_id, sample_id);
        for(var i = 0; i<sample_id_arr.length; i++){
            sample_id_arr[i].style.display = 'inline';
        }
        old_sample_id = sample_id;
        //sample_s.style.display = "inline";
}

for(var i=0; i<3; i++){
    $('input:radio[name="stem"]')[i].addEventListener("change",function(){
        if (this.checked) {
            console.log("botao apertooooo 1");
            stem_value = this.value;
            update_sample_audio();
        }
    });
}

for(var i=0; i<2; i++){
    $('input:radio[name="track"]')[i].addEventListener("change",function(){
        if (this.checked) {
            track_value = this.value;
            console.log("botao apertooooo 2");
            update_sample_audio();
        }
    });
}
    






/*
function verifyCheck(arr){
    for (var i = 0; i < arr.length; i++) {
        if (arr[i].type === 'radio' && arr[i].checked) {
            return true; 
        }
    }
    return false;
}
        
if(verifyCheck(document.getElementsByName('track'))){
    for (var i = 0; i < track.length; i++) {
        if (track[i].type === 'radio' && track[i].checked) {
            track_value = track[i].value;       
        }
    }
    update_sample_audio()
}

if(verifyCheck(document.getElementsByName('stem'))){
    for (var i = 0; i < stem.length; i++) {
        if (stem[i].type === 'radio' && stem[i].checked) {
            stem_value = stem[i].value;       
        }
    }
    update_sample_audio()
}
*/