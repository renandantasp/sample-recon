
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
