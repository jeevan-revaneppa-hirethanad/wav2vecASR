let start = document.getElementById('start')
let result = document.getElementById("output")

let recognition = new webkitSpeechRecognition() || new SpeechRecognition()
recognition.lang= "hi-IN"
recognition.interimResults = true

start.addEventListener('click',()=>{
    recognition.start();
})


recognition.addEventListener('audiostart',(e)=>{
    start.innerText = "Listening.."
})

recognition.addEventListener('result',(e)=>{
    let text = "";
    let i = 0;
    while(i< e.results.length){
        text = e.results[i][0].transcript;
        i++;
    }
    result.innerText = text
})

recognition.addEventListener('audioend',(e)=>{
    start.innerText = "Start"
})