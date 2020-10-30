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