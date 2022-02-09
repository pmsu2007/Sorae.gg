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

/*
룬 정보
8000 : 정밀 (2)
8100 : 지배 (0)
8200 : 마법 (4)
8300 : 영감 (1)
8400 : 결의 (3)
*/

const RUNE_DICT = {
    '8000':2,
    '8100':0,
    '8200':4,
    '8300':1,
    '8400':3, 
}

var ITEM_DATA;
var SPELL_DATA;
var RUNE_DATA;

fetch(STATIC_URL + 'js/item.json')
.then (response => response.json())
.then(
    data => ITEM_DATA = data
)
fetch(STATIC_URL + 'js/summoner.json')
.then (response => response.json())
.then(
    data => SPELL_DATA = data
)
fetch(STATIC_URL + 'js/runesReforged.json')
.then (response => response.json())
.then(
    data => RUNE_DATA = data
)



const cards = document.querySelectorAll('.card');
const detailContainer = document.querySelector('.detail-container');
const records = document.querySelector('.record');

const redTeamTable = document.querySelector('.red-team tbody'); // 5개의 tr
const blueTeamTable = document.querySelector('.blue-team tbody'); // 5개의 tr

const getDetail = function(matchID, matchTime) {
    url = '/detail/' + '?matchID=' +  matchID

    const MATCH_MIN =  matchTime / 60;
    
    fetch(url)
    .then(res => res.json())
    .then(
        json => {
            detailContainer.innerHTML = json.data;
        }
    )
    .then (
        () => {
            detailContainer.querySelectorAll('.game-result').forEach( elem => {
                if (elem.textContent === "승리") elem.style.color = "royalblue";
                else elem.style.color = "crimson";
            })
        })
    .then (
        // set champion image
        () => {
            const championImg = detailContainer.querySelectorAll('.img-level img');
            championImg.forEach(img => {
                img.src = STATIC_URL + 'images/champion/' + img.alt +'.png';
            });
        }
    )
    .then (
        // spell manipulation
        () => {
            const spells = detailContainer.querySelectorAll('.spell');
            spells.forEach(spell => {
                const spellName = SPELL_DICT[spell.dataset.id];
                spell.src = SPELL_URL + spellName  + '.png';
                spell.dataset.tippyContent = SPELL_DATA['data'][spellName]['name'] + '<br><br>'
                + SPELL_DATA['data'][spellName]['description'];
            })
        }
    )
    .then (
        // rune manipulation
        () => {
            const subRunes = detailContainer.querySelectorAll('.s-rune');
            subRunes.forEach(rune => {
                rune.src = STATIC_URL + 'images/' + RUNE_DATA[RUNE_DICT[rune.dataset.id]].icon;
            })
            const primaryRunes = detailContainer.querySelectorAll('.p-rune');
            primaryRunes.forEach(rune => {
                for (let i = 0; i < 5; i++) {
                const slot = RUNE_DATA[i].slots[0].runes;
                slot.forEach(r => {
                    if (r.id == rune.dataset.id) {
                        rune.src = STATIC_URL + 'images/' + r.icon;
                        rune.dataset.tippyContent = r.name + '<br>' + r.shortDesc;
                        return false;
                    }
                })
            }
            })
        }
    )
    .then (            
        // KDA manipulation
        () => {

            const redTeam = document.querySelector('.red-team');
            const blueTeam = document.querySelector('.blue-team');
            
            blueTotalKill = 0;
            redTotalKill = 0;

            blueTeam.querySelectorAll('.kda-num').forEach(elem => {
                let kda = elem.nextElementSibling.firstElementChild.textContent.split('/');
                blueTotalKill += parseInt(kda[0]);
                let kdaNum = (parseInt(kda[0]) + parseInt(kda[2])) / parseInt(kda[1]);
                if (kdaNum !== Infinity) {
                kdaNum = kdaNum.toFixed(2);
                elem.textContent = kdaNum + ':1';
                if (kdaNum >= 5) elem.classList.add('highlight2');
                else if (kdaNum >= 4) elem.classList.add('highlight3');
                else if (kdaNum >= 3) elem.classList.add('highlight4');
                else if (kdaNum < 2) elem.classList.add('highlight5'); 
                } else {
                    elem.textContent = 'Perfect';
                    elem.classList.add('highlight1');
                }
            })
            redTeam.querySelectorAll('.kda-num').forEach(elem => {
                let kda = elem.nextElementSibling.firstElementChild.textContent.split('/');
                redTotalKill += parseInt(kda[0]);
                let kdaNum = (parseInt(kda[0]) + parseInt(kda[2])) / parseInt(kda[1]);
                if (kdaNum !== Infinity) {
                    kdaNum = kdaNum.toFixed(2);
                    elem.textContent = kdaNum + ':1';
                    if (kdaNum >= 5) elem.classList.add('highlight2');
                    else if (kdaNum >= 4) elem.classList.add('highlight3');
                    else if (kdaNum >= 3) elem.classList.add('highlight4');
                    else elem.classList.add('highlight5'); 
                    } else {
                        elem.textContent = 'Perfect';
                        elem.classList.add('highlight1');
                    } 
            })
            blueTeam.querySelectorAll('.kda-detail').forEach(elem => {
                let kda = elem.firstElementChild.textContent.split('/');
                let killParticipation = blueTotalKill != 0 ? Math.round(100 * (parseInt(kda[0]) + parseInt(kda[2])) / blueTotalKill) : 0;
                killPartElem = elem.firstElementChild.nextElementSibling;
                killPartElem.textContent = '(' + killParticipation + '%)';
                if (killParticipation >= 80) killPartElem.classList.add('highlight1');
                else if (killParticipation >= 70) killPartElem.classList.add('highlight2');
                else if (killParticipation >= 60) killPartElem.classList.add('highlight4');
                else if (killParticipation < 50) killPartElem.classList.add('highlight5');
            })
            redTeam.querySelectorAll('.kda-detail').forEach(elem => {
                let kda = elem.firstElementChild.textContent.split('/');
                let killParticipation = redTotalKill != 0 ? Math.round(100 * (parseInt(kda[0]) + parseInt(kda[2])) / redTotalKill) : 0;
                killPartElem = elem.firstElementChild.nextElementSibling;
                killPartElem.textContent = '(' + killParticipation + '%)';
                if (killParticipation >= 80) killPartElem.classList.add('highlight1');
                else if (killParticipation >= 70) killPartElem.classList.add('highlight2');
                else if (killParticipation >= 60) killPartElem.classList.add('highlight4');
                else if (killParticipation < 50) killPartElem.classList.add('highlight5');
            })
        })
    .then (
        // damage manipulation
        () => {
            let damages = detailContainer.querySelectorAll('.damage-info');
            damages = [...damages];
            damages.sort((a, b) => {
                let aDamage = parseInt(a.firstElementChild.dataset.val);
                let bDamage = parseInt(b.firstElementChild.dataset.val);
                return bDamage - aDamage;
            })
            let counter = 1;
            damages.forEach(elem => {
                elem.firstElementChild.nextElementSibling.textContent = counter + '등';
                counter++;
            })
            for (let i = 1; i <= 3; i++) {
                damages[i - 1].classList.add('highlight' + i);
            }
        }
    )
    .then (
        // vision score manipulation
        () => {
            const visions = detailContainer.querySelectorAll('.vision-info');
            visions.forEach(elem => {
                const visionScore = parseInt(elem.firstElementChild.textContent);
                let visionPerMin = visionScore / MATCH_MIN;
                visionPerMin = visionPerMin.toFixed(2);
                const visionPerMinElem = elem.firstElementChild.nextElementSibling;
                visionPerMinElem.textContent = visionPerMin + ' vision/분';

                if (visionPerMin >= 3) visionPerMinElem.classList.add('highlight1');
                else if (visionPerMin >= 2.5) visionPerMinElem.classList.add('highlight2');
                else if (visionPerMin >= 2) visionPerMinElem.classList.add('highlight3');
                else if (visionPerMin >= 1.5) visionPerMinElem.classList.add('highlight4');
                else if (visionPerMin < 1) visionPerMinElem.classList.add('highlight5');
            })
        }
    )
    .then (
        // cs manipulation 
        () => {
            const csElems = detailContainer.querySelectorAll('.cs-info');
            csElems.forEach(elem => {
                const cs = parseInt(elem.firstElementChild.textContent);
                let csPerMin = cs / MATCH_MIN;
                csPerMin = csPerMin.toFixed(1);
                const csPerMinElem = elem.firstElementChild.nextElementSibling;
                csPerMinElem.textContent = csPerMin + 'cs/분';

                if (csPerMin >= 9) csPerMinElem.classList.add('highlight1');
                else if (csPerMin >= 8) csPerMinElem.classList.add('highlight3');
                else if (csPerMin >= 7) csPerMinElem.classList.add('highlight4');
                else if (csPerMin < 6) csPerMinElem.classList.add('highlight5');
            })
        }
    )
    .then (
        // item tooltip
        () => {
            itemImgs = detailContainer.querySelectorAll('.items img');
            itemImgs.forEach(item => {
                item.dataset.tippyContent = ITEM_DATA['data'][item.dataset.id]['name'] + '<br><br>'
                + ITEM_DATA['data'][item.dataset.id]['description'] + '<br>'
                +ITEM_DATA['data'][item.dataset.id]['plaintext']
            })
        }
    )
    .then (
        // tooltip on
        () => {
            $(function () {
                $(".tooltip-div").tooltip();
            });
            const config = {
                arrow: true,
                flipOnUpdate: true,
                interactive: false,
                boundary: 'viewport',
                // popperOptions: {
                //    placement: 'auto'
                // },
                placement: 'auto',
                theme: 'light-border',
                zIndex: 999999
            };
            
            tippy('[data-tippy-content]', config);
        }
        
    )
    .catch(
        function(error) {
            alert('세부전적 불러오기에 실패했습니다.')
        }
    )
    

    

    // manipulate KDA

}

// const calDetail = function()

records.addEventListener('click', function (e) {
    let card = e.target.closest('.card');
    if (!card) return;
    if (!records.contains(card)) return;


    getDetail(card.dataset['matchId'], card.dataset['matchTime']);
    
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

