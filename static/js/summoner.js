const winLoseToNum = function(elem) {
    // change win(or lose) info string to number
    let res;
    res = elem.textContent
    res = parseInt(String.prototype.slice.call(res, 0, -1));
    return res;
}

// calculate solo-rank win ratio and set rank emblem
if (document.querySelector('.soloWin')) {
    // if player has solo rank tier
const soloWin = winLoseToNum(document.querySelector('.soloWin'));
const soloLose = winLoseToNum(document.querySelector('.soloLose'));

const soloWinRatio = soloWin == 0 ? 0 : Math.round(100 * soloWin / (soloWin + soloLose));

let ratioElem = document.querySelector('.soloWinRatio');
ratioElem.textContent += soloWinRatio.toString() + '%';

// set image
let tierImg = document.querySelector('.soloImg');
const tier = document.querySelector('.soloRank').textContent.toLowerCase();
tierImg.setAttribute('src', DJANGO_STATIC_URL + 'images/ranked-emblems/' + tier + '.png');
tierImg.setAttribute('alt', tier);
}

// calculate free-rank win ratio and set rank emblem
if (document.querySelector('.freeWin')) {
    // if player has free rank tier
const freeWin = winLoseToNum(document.querySelector('.freeWin'));
const freeLose = winLoseToNum(document.querySelector('.freeLose'));

const freeWinRatio = freeWin == 0 ? 0 : Math.round(100 * freeWin / (freeWin + freeLose));

let ratioElem = document.querySelector('.freeWinRatio');
ratioElem.textContent += freeWinRatio.toString() + '%';

// set image
let tierImg = document.querySelector('.freeImg');
const tier = document.querySelector('.freeRank').textContent.toLowerCase();
tierImg.setAttribute('src', DJANGO_STATIC_URL + 'images/ranked-emblems/' + tier + '.png');
tierImg.setAttribute('alt', tier);
}
