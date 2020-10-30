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
