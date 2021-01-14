const Http = new XMLHttpRequest();
const state_url = '/state';
var state = false;
$(document).ready(function(){
    window.clearInterval()
    window.setInterval(function(){
        Http.open('GET', state_url);
        Http.send();
        Http.onreadystatechange = (e) => {
            if (Http.responseText) {
                state = JSON.parse(Http.responseText)
                console.log(state.established)
                if (state.established == false) {
                    $('.bg-model').show(300)
                } else {
                    $('.bg-model').hide(300)
                }
            }
        }
    }, 1000);
})

