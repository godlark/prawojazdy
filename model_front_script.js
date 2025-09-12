function updateInput(value) {
    // To make it Desktop Anki comptabile
    let typeans = document.getElementById('typeans');
    typeans.value = value;

    // To make it AnkiDroid compatible
    if (typeof taChange === 'function') {
        taChange(typeans);
    }
    if (typeof taKey === 'function') {
        taKey(typeans, {key: ''});
    }
}

{
    let video = document.querySelector(".media-wrapper video");
    let timer1 = document.querySelector('.timer1');
    let timer2 = document.querySelector('.timer2');
    timer1.addEventListener('animationend', () => {
        if (video) {
            video.play();
        } else {
            timer2.classList.add('animate');
        }
    });
    if (video) {
        video.addEventListener('ended', () => {
            timer2.classList.add('animate');
        });
    }
}