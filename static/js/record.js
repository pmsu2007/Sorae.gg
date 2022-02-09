// coloring card! win -> royalblue, lose -> crimson
const CHAMP_URL ="https://ddragon.leagueoflegends.com/cdn/12.3.1/img/champion/";
const SPELL_URL ="https://ddragon.leagueoflegends.com/cdn/12.3.1/img/spell/";
const SPELL_DICT = {
'21': 'SummonerBarrier',
'1': 'SummonerBoost',
'14': 'SummonerDot',
'3': 'SummonerExhaust',
'4': 'SummonerFlash',
'6': 'SummonerHaste',
'7': 'SummonerHeal',
'13': 'SummonerMana',
'30': 'SummonerPoroRecall',
'31': 'SummonerPoroThrow',
'11': 'SummonerSmite',
'39': 'SummonerSnowURFSnowball_Mark',
'32': 'SummonerSnowball',
'12': 'SummonerTeleport',
'54': 'Summoner_UltBookPlaceholder',
'55': 'Summoner_UltBookSmitePlaceholder',
}

const cards = document.querySelectorAll('.card');
const detailContainer = document.querySelector('.detail-container');
const records = document.querySelector('.record');
const redTeam = document.querySelector('red-team');
const blueTeam = document.querySelector('blue-team');
const redTeamTable = document.querySelector('.red-team tbody'); // 5개의 tr
const blueTeamTable = document.querySelector('.blue-team tbody'); // 5개의 tr

const makeRow = function(data) {
    let row = document.querySelector('.sample-row').cloneNode(true);

    const champImg = row.querySelector('.champ');
    champImg.src = CHAMP_URL + data['champ_name'];

    const champLevel = row.querySelector('.champ-info .level');
    champLevel.textContent = data['champ_level'];

    const spellBox = row.querySelector('.spell-box');
    spellBox.children[0].src = SPELL_URL + SPELL_DICT[data['spell1']] + '.png';
    spellBox.children[1].src = SPELL_URL + SPELL_DICT[data['spell2']] + '.png';

    const runeBox = row.querySelector('.rune-box');
    runeBox.children[0].src;

    const summonerName = row.querySelector('.summoner-name');
    summonerName.firstElementChild.href="./?usrName="+data['summoner_name'];
    summonerName.firstElementChild.textContent = data['summoner_name'];
}
const getDetail = function(matchID) {
    url = '//url' + '?matchID=' +  matchID

    fetch(url)
    .then(JSON.parse)
    .then(
        data => {
            redTeamTable.innerHTML = '';
            blueTeamTable.innerHTML = '';
            for (let i = 0; i < data.length/2; i++) { // red team
                redTeamTable.appendChild(makeRow(data[i]));
            }
        }
    )
    .catch(alert('전적을 불러오기에 실패했습니다.'))
}

records.addEventListener('click', function (e) {
    let card = e.target.closest('.card');
    if (!card) return;
    if (!records.contains(card)) return;


    // getDetail(card.dataset['matchId']);
    
});

[...cards].forEach(card => {
    if (card.dataset.result == 'True') {
        card.classList.add('card-win');
    } else {
        card.classList.add('card-lose');
    }
})

// tooltip initial

$(function () {
    $(".tooltip-div").tooltip();
});

